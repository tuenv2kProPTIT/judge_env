

"""C++17 programming language definition."""
from .base import CompiledLanguage


__all__ = ["Cpp17Gpp"]


class Cpp17Gpp(CompiledLanguage):
    """This defines the C++ programming language, compiled with g++ (the
    version available on the system) using the C++17 standard.

    """

    @property
    def name(self):
        """See Language.name."""
        return "C++17 / g++"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".cpp", ".cc", ".cxx", ".c++", ".C"]

    @property
    def header_extensions(self):
        """See Language.header_extensions."""
        return [".h"]

    @property
    def object_extensions(self):
        """See Language.object_extensions."""
        return [".o"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        command = ["/usr/bin/g++"]
        if for_evaluation:
            command += ["-DEVAL"]
        command += ["-std=gnu++17", "-O2", "-pipe", "-static",
                    "-s", "-o", executable_filename]
        command += source_filenames 
        return [command]
