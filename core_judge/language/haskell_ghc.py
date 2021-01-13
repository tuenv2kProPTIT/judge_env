

"""Haskell programming language definition."""

import os

from .base import CompiledLanguage


__all__ = ["HaskellGhc"]


class HaskellGhc(CompiledLanguage):
    """This defines the Haskell programming language, compiled with ghc
    (the version available on the system).

    """

    @property
    def name(self):
        """See Language.name."""
        return "Haskell / ghc"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".hs"]

    @property
    def object_extensions(self):
        """See Language.source_extensions."""
        return [".o"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        commands = []
        # Haskell module names are capitalized, so we change the source file
        # names (except for the first one) to match the module's name.
        # The first source file is, instead, the grader or the standalone
        # source file; it won't be imported in any other source file, so
        # there is no need to capitalize it.
        for source in source_filenames[1:]:
            commands.append(["/bin/ln", "-s", os.path.basename(source),
                             HaskellGhc._capitalize(source)])
        commands.append(["/usr/bin/ghc", "-static", "-O2", "-Wall", "-o",
                         executable_filename, source_filenames[0]])
        return commands

    @staticmethod
    def _capitalize(string):
        dirname, basename = os.path.split(string)
        return os.path.join(dirname, basename[0].upper() + basename[1:])
