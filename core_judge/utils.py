import argparse
import grp
import itertools
import logging
# import netifaces
import os
import stat
import sys


import gevent
import gevent.socket
from shlex import quote




def pretty_print_cmdline(cmdline):
    """Pretty print a command line.
    Take a command line suitable to be passed to a Popen-like call and
    returns a string that represents it in a way that preserves the
    structure of arguments and can be passed to bash as is.
    More precisely, delimitate every item of the command line with
    single apstrophes and join all the arguments separating them with
    spaces.
    """
    return " ".join(quote(x) for x in cmdline)
    
def mkdir(path):
    """Make a directory without complaining for errors.

    path (string): the path of the directory to create
    returns (bool): True if the dir is ok, False if it is not

    """
    try:
        os.mkdir(path)
    except FileExistsError:
        return True
    except OSError:
        return False
    else:
        try:
            os.chmod(path, 0o770)
        except OSError:
            os.rmdir(path)
            return False
        else:
            return True


# This function uses os.fwalk() to avoid the symlink attack, see:
# - https://bugs.python.org/issue4489
# - https://bugs.python.org/issue13734
def rmtree(path):
    """Recursively delete a directory tree.

    Remove the directory at the given path, but first remove the files
    it contains and recursively remove the subdirectories it contains.
    Be cooperative with other greenlets by yielding often.

    path (str): the path to a directory.

    raise (OSError): in case of errors in the elementary operations.

    """
    # If path is a symlink, fwalk() yields no entries.
    for _, subdirnames, filenames, dirfd in os.fwalk(path, topdown=False):
        for filename in filenames:
            os.remove(filename, dir_fd=dirfd)
            gevent.sleep(0)
        for subdirname in subdirnames:
            if stat.S_ISLNK(os.lstat(subdirname, dir_fd=dirfd).st_mode):
                os.remove(subdirname, dir_fd=dirfd)
            else:
                os.rmdir(subdirname, dir_fd=dirfd)
            gevent.sleep(0)

    # Remove the directory itself. An exception is raised if path is a symlink.
    os.rmdir(path)
