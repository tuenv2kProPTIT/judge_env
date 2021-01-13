#!/usr/bin/env python3



"""C programming language definition."""

from .base import CompiledLanguage


__all__ = ["C11Gcc"]


class C11Gcc(CompiledLanguage):
    """This defines the C programming language, compiled with gcc (the
    version available on the system) using the C11 standard.

    """

    @property
    def name(self):
        """See Language.name."""
        return "C11 / gcc"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".c"]

    @property
    def header_extensions(self):
        """See Language.source_extensions."""
        return [".h"]

    @property
    def object_extensions(self):
        """See Language.source_extensions."""
        return [".o"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        command = ["/usr/bin/gcc"]
        if for_evaluation:
            command += ["-DEVAL"]
        command += ["-std=gnu11", "-O2", "-pipe", "-static",
                    "-s", "-o", executable_filename]
        command += source_filenames
        command += ["-lm"]
        return [command]
