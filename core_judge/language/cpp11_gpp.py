#!/usr/bin/env python3



"""C++11 programming language definition."""
from .base import CompiledLanguage


__all__ = ["Cpp11Gpp"]


class Cpp11Gpp(CompiledLanguage):
    """This defines the C++ programming language, compiled with g++ (the
    version available on the system) using the C++11 standard.

    """

    @property
    def name(self):
        """See Language.name."""
        return "C++11 / g++"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".cpp", ".cc", ".cxx", ".c++", ".C"]

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
        command = ["/usr/bin/g++"]
        if for_evaluation:
            command += ["-DEVAL"]
        command += ["-std=gnu++11", "-O2", "-pipe", "-static",
                    "-s", "-o", executable_filename]
        command += [source_filenames] if isinstance(source_filenames,str) else source_filenames
        return [command]
