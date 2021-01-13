
import io
import logging
import os
import resource
import select
import stat
import tempfile
from abc import ABCMeta, abstractmethod
from functools import wraps, partial

import gevent
from gevent import subprocess
import time

# from fake_conf import config,rmtree,monotonic_time,pretty_print_cmdline
try:
    from ..config import env
except:
    from config import env
logging.basicConfig(level=env.level_logging)
logger = logging.getLogger(__name__)


class SandboxInterfaceException(Exception):
    pass


def with_log(func):
    """Decorator for presuming that the logs are present.

    """
    @wraps(func)
    def newfunc(self, *args, **kwargs):
        """If they are not present, get the logs.

        """
        if self.log is None:
            self.get_log()
        return func(self, *args, **kwargs)

    return newfunc


def wait_without_std(procs,enable=False):
    """Wait for the conclusion of the processes in the list, avoiding
    starving for input and output.

    procs (list): a list of processes as returned by Popen.

    return (list): a list of return codes.

    """
    if len(procs) == 1:
        stdout, stderr = procs[0].communicate()
        returncode =procs[0].returncode
        return [returncode]
    def get_to_consume():
        """Amongst stdout and stderr of list of processes, find the
        ones that are alive and not closed (i.e., that may still want
        to write to).

        return (list): a list of open streams.

        """
        to_consume = []
        # stdin = []
        for process in procs:
            if process.poll() is None:  # If the process is alive.
                if process.stdout and not process.stdout.closed:
                    to_consume.append(process.stdout)
                if process.stderr and not process.stderr.closed:
                    to_consume.append(process.stderr)
                # if process.stdin and not process.stdin.closed:
                    # stdin.append(process.stdin)
        return to_consume

    # Close stdin; just saying stdin=None isn't ok, because the
    # standard input would be obtained from the application stdin,
    # that could interfere with the child process behaviour
    

    # Read stdout and stderr to the end without having to block
    # because of insufficient buffering (and without allocating too
    # much memory). Unix specific.
    if not enable:
        for process in procs:
                if process.stdin:
                    process.stdin.close()
    to_consume = get_to_consume()
    
    while len(to_consume) > 0:
        to_read = select.select(to_consume, [],[], 0.5)[0]
        for file_ in to_read:
            file_.read(8 * 1024)
        to_consume = get_to_consume()
    return [process.wait() for process in procs]


class Truncator(io.RawIOBase):
    """Wrap a file-like object to simulate truncation.

    This file-like object provides read-only access to a limited prefix
    of a wrapped file-like object. It provides a truncated version of
    the file without ever touching the object on the filesystem.

    This class is only able to wrap binary streams as it relies on the
    readinto method which isn't provided by text (unicode) streams.

    """
    def __init__(self, fobj, size):
        """Wrap fobj and give access to its first size bytes.

        fobj (fileobj): a file-like object to wrap.
        size (int): the number of bytes that will be accessible.

        """
        self.fobj = fobj
        self.size = size

    def close(self):
        """See io.IOBase.close."""
        self.fobj.close()

    @property
    def closed(self):
        """See io.IOBase.closed."""
        return self.fobj.closed

    def readable(self):
        """See io.IOBase.readable."""
        return True

    def seekable(self):
        """See io.IOBase.seekable."""
        return True

    def readinto(self, b):
        """See io.RawIOBase.readinto."""
        # This is the main "trick": we clip (i.e. mask, reduce, slice)
        # the given buffer so that it doesn't overflow into the area we
        # want to hide (that is, out of the prefix) and then we forward
        # it to the wrapped file-like object.
        b = memoryview(b)[:max(0, self.size - self.fobj.tell())]
        return self.fobj.readinto(b)

    def seek(self, offset, whence=io.SEEK_SET):
        """See io.IOBase.seek."""
        # We have to catch seeks relative to the end of the file and
        # adjust them to the new "imposed" size.
        if whence == io.SEEK_END:
            if self.fobj.seek(0, io.SEEK_END) > self.size:
                self.fobj.seek(self.size, io.SEEK_SET)
            return self.fobj.seek(offset, io.SEEK_CUR)
        else:
            return self.fobj.seek(offset, whence)

    def tell(self):
        """See io.IOBase.tell."""
        return self.fobj.tell()

    def write(self, _):
        """See io.RawIOBase.write."""
        raise io.UnsupportedOperation('write')