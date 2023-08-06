import collections
import functools
import importlib
import mimetypes
import os
from pathlib import Path
import queue
import re
import threading
import warnings

from watchgod.watcher import RegExpWatcher, Change

from ..structures.dataframe import XLSX_MIME_TYPE
from ..utils import CachingMap, import_object, OneShotCachedMap
from .in_memory import Tree as TreeInMemory


class Tree(TreeInMemory):
    """
    A Tree constructed by walking a directory and watching it for changes.

    Examples
    --------

    >>> Tree.from_directory("path/to/directory")
    """

    __slots__ = (
        "_watcher_thread_kill_switch",
        "_index",
        "_directory",
        "_manual_trigger",
    )

    # This maps MIME types (i.e. file formats) for appropriate Readers.
    # OneShotCachedMap is used to defer imports. We don't want to pay up front
    # for importing Readers that we will not actually use.
    DEFAULT_READERS_BY_MIMETYPE = OneShotCachedMap(
        {
            "image/tiff": lambda: importlib.import_module(
                "...readers.tiff", Tree.__module__
            ).TiffReader,
            "text/csv": lambda: importlib.import_module(
                "...readers.dataframe", Tree.__module__
            ).DataFrameAdapter.read_csv,
            XLSX_MIME_TYPE: lambda: importlib.import_module(
                "...readers.excel", Tree.__module__
            ).ExcelReader.from_file,
            "application/x-hdf5": lambda: importlib.import_module(
                "...readers.hdf5", Tree.__module__
            ).HDF5Reader.from_file,
        }
    )

    # We can mostly rely on mimetypes.types_map for the common ones
    # ('.csv' -> 'text/csv', etc.) but we supplement here for some
    # of the more exotic ones that not all platforms know about.
    DEFAULT_MIMETYPES_BY_FILE_EXT = {
        # This is the "official" file extension.
        ".h5": "application/x-hdf5",
        # This is NeXus. We may want to invent a special media type
        # like 'application/x-nexus' for this, but I'll punt that for now.
        # Needs thought about how to encode the various types of NeXus
        # (media type arguments, for example).
        ".nxs": "application/x-hdf5",
        # These are unofficial but common file extensions.
        ".hdf": "application/x-hdf5",
        ".hdf5": "application/x-hdf5",
    }

    @classmethod
    def from_directory(
        cls,
        directory,
        *,
        ignore_re_dirs=None,
        ignore_re_files=None,
        readers_by_mimetype=None,
        mimetypes_by_file_ext=None,
        key_from_filename=None,
        metadata=None,
        access_policy=None,
        authenticated_identity=None,
        error_if_missing=True,
        **kwargs,
    ):
        if error_if_missing:
            if not os.path.isdir(directory):
                raise ValueError(
                    f"{directory} is not a directory. "
                    "To run anyway, in anticipation of the directory "
                    "appearing later, use error_if_missing=False."
                )
        readers_by_mimetype = readers_by_mimetype or {}
        # If readers_by_mimetype comes from a configuration file,
        # objects are given as importable strings, like "package.module:Reader".
        for key, value in list(readers_by_mimetype.items()):
            if isinstance(value, str):
                readers_by_mimetype[key] = import_object(value)
        # User-provided readers take precedence over defaults.
        merged_readers_by_mimetype = collections.ChainMap(
            readers_by_mimetype, cls.DEFAULT_READERS_BY_MIMETYPE
        )
        mimetypes_by_file_ext = mimetypes_by_file_ext or {}
        merged_mimetypes_by_file_ext = collections.ChainMap(
            mimetypes_by_file_ext, cls.DEFAULT_MIMETYPES_BY_FILE_EXT
        )
        if key_from_filename is None:

            def key_from_filename(filename):
                # identity
                return filename

        # Map subdirectory path parts, as in ('a', 'b', 'c'), to mapping of partials.
        # This single index represents the entire nested directory structure. (We
        # could have done this recursively, with each sub-Tree watching its own
        # subdirectory, but there are efficiencies to be gained by doing a single
        # walk of the nested directory structure and having a single thread watching
        # for changes within that structure.)
        index = {(): {}}
        # 1. Start watching directory for changes and accumulating a queue of them.
        # 2. Do an initial scan of the files in the directory.
        # 3. When the initial scan completes, start processing changes. This
        #    will cover changes that occurred during or after the initial scan and
        #    avoid a possibile a race condition.
        initial_scan_complete = []
        watcher_thread_kill_switch = []
        manual_trigger = queue.Queue()
        watcher_thread = threading.Thread(
            target=_watch,
            args=(
                directory,
                ignore_re_files,
                ignore_re_dirs,
                index,
                merged_readers_by_mimetype,
                merged_mimetypes_by_file_ext,
                key_from_filename,
                initial_scan_complete,
                watcher_thread_kill_switch,
                manual_trigger,
            ),
            daemon=True,
            name="tiled-watch-filesystem-changes",
        )
        watcher_thread.start()
        compiled_ignore_re_dirs = (
            re.compile(ignore_re_dirs) if ignore_re_dirs is not None else ignore_re_dirs
        )
        compiled_ignore_re_files = (
            re.compile(ignore_re_files)
            if ignore_re_files is not None
            else ignore_re_files
        )
        for root, subdirectories, files in os.walk(directory, topdown=True):
            parts = Path(root).relative_to(directory).parts
            # Account for ignore_re_dirs and update which subdirectories we will traverse.
            valid_subdirectories = []
            for d in subdirectories:
                if (ignore_re_dirs is None) or compiled_ignore_re_dirs.match(
                    str(Path(*(parts + (d,))))
                ):
                    valid_subdirectories.append(d)
            subdirectories[:] = valid_subdirectories
            for subdirectory in subdirectories:
                # Make a new mapping and a corresponding Tree for this subdirectory.
                mapping = {}
                index[parts + (subdirectory,)] = mapping
                index[parts][subdirectory] = functools.partial(
                    TreeInMemory, CachingMap(mapping)
                )
            # Account for ignore_re_files and update which files we will traverse.
            valid_files = []
            for f in files:
                if (ignore_re_files is None) or compiled_ignore_re_files.match(
                    str(Path(*(parts + (f,))))
                ):
                    valid_files.append(f)
            files[:] = valid_files
            for filename in files:
                if (ignore_re_files is not None) and compiled_ignore_re_files.match(
                    str(Path(*parts))
                ):
                    continue
                # Add items to the mapping for this root directory.
                try:
                    key = key_from_filename(filename)
                    index[parts][key] = _reader_factory_for_file(
                        merged_readers_by_mimetype,
                        merged_mimetypes_by_file_ext,
                        Path(root, filename),
                    )
                except NoReaderAvailable:
                    pass
        # Appending any object will cause bool(initial_scan_complete) to
        # evaluate to True.
        initial_scan_complete.append(object())
        mapping = CachingMap(index[()])
        return cls(
            mapping,
            directory=directory,
            index=index,
            watcher_thread_kill_switch=watcher_thread_kill_switch,
            manual_trigger=manual_trigger,
            metadata=metadata,
            authenticated_identity=authenticated_identity,
            access_policy=access_policy,
            # The __init__ of this class does not accept any other
            # kwargs, but subclasses can use this to set up additional
            # instance state.
            **kwargs,
        )

    def __init__(
        self,
        mapping,
        directory,
        index,
        watcher_thread_kill_switch,
        manual_trigger,
        metadata,
        access_policy,
        authenticated_identity,
    ):
        super().__init__(
            mapping,
            metadata=metadata,
            access_policy=access_policy,
            authenticated_identity=authenticated_identity,
        )
        self._directory = directory
        self._index = index
        self._watcher_thread_kill_switch = watcher_thread_kill_switch
        self._manual_trigger = manual_trigger

    def update_now(self):
        "Force an update and block until it completes."
        event = threading.Event()
        self._manual_trigger.put(event)
        # The worker thread will set this Event when processing completes.
        # Wait on that, and the return.
        event.wait()

    @property
    def directory(self):
        return self._directory

    def new_variation(self, *args, **kwargs):
        return super().new_variation(
            *args,
            watcher_thread_kill_switch=self._watcher_thread_kill_switch,
            manual_trigger=self._manual_trigger,
            directory=self._directory,
            index=self._index,
            **kwargs,
        )

    def shutdown_watcher(self):
        # Appending any object will cause bool(self._watcher_thread_kill_switch)
        # to evaluate to True.
        self._watcher_thread_kill_switch.append(object())


def _watch(
    directory,
    ignore_re_files,
    ignore_re_dirs,
    index,
    readers_by_mimetype,
    mimetypes_by_file_ext,
    key_from_filename,
    initial_scan_complete,
    watcher_thread_kill_switch,
    manual_trigger,
    poll_interval=0.2,
):
    watcher = RegExpWatcher(
        directory,
        re_files=ignore_re_files,
        re_dirs=ignore_re_dirs,
    )
    queued_changes = []
    event = None
    while not watcher_thread_kill_switch:
        changes = watcher.check()
        if initial_scan_complete:
            # Process initial backlog. (This only happens once, ever.)
            if queued_changes:
                _process_changes(
                    queued_changes,
                    directory,
                    readers_by_mimetype,
                    mimetypes_by_file_ext,
                    key_from_filename,
                    index,
                )
            # Process changes just collected.
            _process_changes(
                changes,
                directory,
                readers_by_mimetype,
                mimetypes_by_file_ext,
                key_from_filename,
                index,
            )
        else:
            # The initial scan is still going. Stash the changes for later.
            queued_changes.extend(changes)
        if event is not None:
            # The processing above was the result of a manual trigger.
            # Confirm to the sender that it has now completed.
            event.set()
        try:
            event = manual_trigger.get(timeout=poll_interval)
        except queue.Empty:
            event = None


def _process_changes(
    changes,
    directory,
    readers_by_mimetype,
    mimetypes_by_file_ext,
    key_from_filename,
    index,
):
    ignore = set()
    for kind, entry in changes:
        path = Path(entry)
        if path in ignore:
            # We have seen this before and could not find a Reader for it.
            # Do not try again.
            continue
        if path.is_dir():
            raise NotImplementedError
        parent_parts = path.relative_to(directory).parent.parts
        if kind == Change.added:
            try:
                key = key_from_filename(path.name)
                index[parent_parts][key] = _reader_factory_for_file(
                    readers_by_mimetype,
                    mimetypes_by_file_ext,
                    path,
                )
            except NoReaderAvailable:
                # Ignore this file in the future.
                # We already know that we do not know how to find a Reader
                # for this filename.
                ignore.add(path)
        elif kind == Change.deleted:
            key = key_from_filename(path.name)
            index[parent_parts].pop(key, None)
        elif kind == Change.modified:
            # Why do we need a try/except here? A reasonable question!
            # Normally, we would learn about the file first via a Change.added
            # or via the initial scan. Then, later, when we learn about modification
            # we can be sure that we already know how to find a Reader for this
            # filename. But, during that initial scan, there is a race condition
            # where we might learn about Change.modified before we first add that file
            # to our index. Therefore, we guard this with a try/except, knowing
            # that this could be the first time we see this path.
            try:
                key = key_from_filename(path.name)
                index[parent_parts][key] = _reader_factory_for_file(
                    readers_by_mimetype,
                    mimetypes_by_file_ext,
                    path,
                )
            except NoReaderAvailable:
                # Ignore this file in the future.
                # We already know that we do not know how to find a Reader
                # for this filename.
                ignore.add(path)


def _reader_factory_for_file(readers_by_mimetype, mimetypes_by_file_ext, path):
    ext = "".join(path.suffixes)  # e.g. ".h5" or ".tar.gz"
    if ext in mimetypes_by_file_ext:
        mimetype = mimetypes_by_file_ext[ext]
    else:
        # Use the Python's built-in facility for guessing mimetype
        # from file extension. This loads data about mimetypes from
        # the operating system the first time it is used.
        mimetype, _ = mimetypes.guess_type(path)
    if mimetype is None:
        msg = (
            f"The file at {path} has a file extension {ext} this is not "
            "recognized. The file will be skipped, pass in a mimetype "
            "for this file extension via the parameter "
            "Tree.from_directory(..., mimetypes_by_file_ext={...}) and "
            "pass in a Reader than handles this mimetype via "
            "the parameter Tree.from_directory(..., readers_by_mimetype={...})."
        )
        warnings.warn(msg)
        raise NoReaderAvailable
    try:
        reader_class = readers_by_mimetype[mimetype]
    except KeyError:
        msg = (
            f"The file at {path} was recognized as mimetype {mimetype} "
            "but there is no reader for that mimetype. The file will be skipped. "
            "To fix this, pass in a Reader than handles this mimetype via "
            "the parameter Tree.from_directory(..., readers_by_mimetype={...})."
        )
        warnings.warn(msg)
        raise NoReaderAvailable
    return functools.partial(reader_class, str(path))


class NoReaderAvailable(Exception):
    pass
