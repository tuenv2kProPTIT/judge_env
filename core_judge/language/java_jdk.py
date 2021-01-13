
"""Java programming language definition, using the default JDK installed
in the system.

"""

from shlex import quote as shell_quote
from .base import CompiledLanguage,Language


__all__ = ["JavaJDK"]


class JavaJDK(Language):
    """This defines the Java programming language, compiled and executed using
    the Java Development Kit available in the system.

    """

    USE_JAR = True

    @property
    def name(self):
        """See Language.name."""
        return "Java / JDK"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".java"]

    @property
    def requires_multithreading(self):
        """See Language.requires_multithreading."""
        return True

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        compile_command = ["/usr/bin/javac"] + source_filenames
        # We need to let the shell expand *.class as javac create
        # a class file for each inner class.
        if JavaJDK.USE_JAR:
            jar_command = ["/bin/sh", "-c",
                           " ".join(["jar", "cf",
                                     shell_quote(executable_filename),
                                     "*.class"])]
            return [compile_command, jar_command]
        else:
            zip_command = ["/bin/sh", "-c",
                           " ".join(["zip", "-r", "-", "*.class", ">",
                                     shell_quote(executable_filename)])]
            return [compile_command, zip_command]

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        args = args if args is not None else []
        if JavaJDK.USE_JAR:
            # executable_filename is a jar file, main is the name of
            # the main java class
            return [["/usr/bin/java", "-Deval=true", "-Xmx512M", "-Xss64M",
                     "-cp", executable_filename, main] + args]
        else:
            unzip_command = ["/usr/bin/unzip", executable_filename]
            command = ["/usr/bin/java", "-Deval=true", "-Xmx512M", "-Xss64M",
                       main] + args
            return [unzip_command, command]
