

"""Pascal programming language definition."""
from .base import CompiledLanguage


__all__ = ["PascalFpc"]


class PascalFpc(CompiledLanguage):
    """This defines the Pascal programming language, compiled with Free
    Pascal (the version available on the system).

    """

    @property
    def name(self):
        """See Language.name."""
        return "Pascal / fpc"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".pas"]

    @property
    def header_extensions(self):
        """See Language.source_extensions."""
        return ["lib.pas"]

    @property
    def object_extensions(self):
        """See Language.source_extensions."""
        return [".o"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        command = ["/usr/bin/fpc"]
        if for_evaluation:
            command += ["-dEVAL"]
        command += ["-O2", "-XSs", "-o%s" % executable_filename]
        command += [source_filenames[0]]
        return [command]
