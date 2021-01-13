

"""C# programming language definition, using the mono compiler "mcs"
and runtime "mono" installed in the system.

"""

from .base import CompiledLanguage,Language


__all__ = ["CSharpMono"]


class CSharpMono(Language):
    """This defines the C# programming language, compiled with the mono
    compiler "mcs" and executed with the runtime "mono".

    """

    @property
    def name(self):
        """See Language.name."""
        return "C# / Mono"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".cs"]

    @property
    def requires_multithreading(self):
        """See Language.requires_multithreading."""
        return True

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        compile_command = ["/usr/bin/mcs",
                           "-out:" + executable_filename,
                           "-optimize+"]
        compile_command += source_filenames
        return [compile_command]

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        return [["/usr/bin/mono", executable_filename]]
