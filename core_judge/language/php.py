

"""PHP programming language definition."""

from .base import CompiledLanguage,Language


__all__ = ["Php"]


class Php(Language):
    """This defines the PHP programming language, interpreted with the
    standard PHP interpreter available in the system.

    """

    @property
    def name(self):
        """See Language.name."""
        return "PHP"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".php"]

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        return [["/bin/cp", source_filenames[0], executable_filename]]

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        args = args if args is not None else []
        return [["/usr/bin/php", executable_filename] + args]
