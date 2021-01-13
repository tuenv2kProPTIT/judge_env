

"""Python programming language, version 2, definition."""

import os

from .base import CompiledLanguage


__all__ = ["Python2CPython"]


class Python2CPython(CompiledLanguage):
    """This defines the Python programming language, version 2 (more
    precisely, the subversion of Python 2 available on the system,
    usually 2.7) using the default interpeter in the system.

    """

    MAIN_FILENAME = "__main__.pyc"

    @property
    def name(self):
        """See Language.name."""
        return "Python 2 / CPython"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".py"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        zip_filename = "%s.zip" % executable_filename

        commands = []
        files_to_package = []
        commands.append(["/usr/bin/python2", "-m", "compileall", "."])
        for idx, source_filename in enumerate(source_filenames):
            basename = os.path.splitext(os.path.basename(source_filename))[0]
            pyc_filename = "%s.pyc" % basename
            # The file with the entry point must be in first position.
            if idx == 0:
                commands.append(["/bin/mv", pyc_filename, self.MAIN_FILENAME])
                files_to_package.append(self.MAIN_FILENAME)
            else:
                files_to_package.append(pyc_filename)

        # zip does not support writing to a file without extension.
        commands.append(["/usr/bin/zip", "-r", zip_filename]
                        + files_to_package)
        commands.append(["/bin/mv", zip_filename, executable_filename])

        return commands

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        args = args if args is not None else []
        return [["/usr/bin/python2", executable_filename] + args]
