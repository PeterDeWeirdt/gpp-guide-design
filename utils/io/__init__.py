import tempfile
import os
from atomicwrites import atomic_write as _backend_writer, AtomicWriter
import io
from contextlib import contextmanager

# You probably need to inspect and override some internals of the package
class SuffixWriter(AtomicWriter):

    def __init__(self, path, mode='w', overwrite=False, as_file=True,
                 **open_kwargs):
        if 'a' in mode:
            raise ValueError(
                'Appending to an existing file is not supported, because that '
                'would involve an expensive `copy`-operation to a temporary '
                'file. Open the file in normal `w`-mode and copy explicitly '
                'if that\'s what you\'re after.'
            )
        if 'x' in mode:
            raise ValueError('Use the `overwrite`-parameter instead.')
        if 'w' not in mode:
            raise ValueError('AtomicWriters can only be written to.')

        self._path = path
        self._mode = mode
        self._overwrite = overwrite
        self._as_file = as_file
        self._open_kwargs = open_kwargs


    def get_fileobject(self, dir=None, **kwargs):
        '''Return the temporary file to use.'''
        filename, file_extension = os.path.splitext(self._path)
        if dir is None:
            dir = os.path.normpath(os.path.dirname(self._path))
        descriptor, name = tempfile.mkstemp(dir=dir, suffix=file_extension)
        # io.open() will take either the descriptor or the name, but we need
        # the name later for commit()/replace_atomic() and couldn't find a way
        # to get the filename from the descriptor.
        os.close(descriptor)
        kwargs['mode'] = self._mode
        kwargs['file'] = name
        return io.open(**kwargs)

    @contextmanager
    def _open(self, get_fileobject):
        f = None  # make sure f exists even if get_fileobject() fails
        try:
            success = False
            with get_fileobject(**self._open_kwargs) as f:
                yield f
                self.sync(f)
            if self._as_file:
                self.commit(f)
            success = True
        finally:
            if not success:
                try:
                    self.rollback(f)
                except Exception:
                    pass

@contextmanager
def atomic_write(file, mode='w', as_file=True, **kwargs):
    """Write a file atomically

            :param file: str or :class:`os.PathLike` target to write
            :param bool as_file:  if True, the yielded object is a :class:File.
                Otherwise, it will be the temporary file path string
            :param mode: str for open, such as 'w' for write
            :param kwargs: anything else needed to open the file

            :raises: FileExistsError if target exists

            Example::

                with atomic_write("hello.txt") as f:
                    f.write("world!")

        """
    with _backend_writer(file, writer_cls=SuffixWriter, mode=mode, as_file=as_file, **kwargs) as f:
        yield f
