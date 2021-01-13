
"""Rust programming language definition."""
from .base import CompiledLanguage


__all__ = ["Rust"]


class Rust(CompiledLanguage):
    """This defines the Rust programming language, compiled with the
    standard Rust compiler available in the system.

    """

    @property
    def name(self):
        """See Language.name."""
        return "Rust"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".rs"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        # In Rust only the source file containing the main function has
        # to be passed to the compiler
        return [["/usr/bin/rustc", "-O", "-o",
                 executable_filename, source_filenames[0]]]
