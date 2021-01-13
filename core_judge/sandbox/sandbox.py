from .sandbox_util import wait_without_std,Truncator,with_log,SandboxInterfaceException

import os
try:
    from ..config import env
    from ..utils import pretty_print_cmdline,rmtree,mkdir
except:
    from config import env
    from utils import pretty_print_cmdline,rmtree,mkdir
from uuid import uuid4
import io
import logging
import os
import io
import logging
import os
import resource
import select
import stat
import tempfile
import time
import shutil
from abc import ABCMeta, abstractmethod
from functools import wraps, partial
from gevent import subprocess

logging.basicConfig(level=env.level_logging)
logger = logging.getLogger(__name__)
class IsolateSandbox(object):
    next_id = 0
    EXIT_SANDBOX_ERROR = 'sandbox error'
    EXIT_OK = 'ok'
    EXIT_SIGNAL = 'signal'
    EXIT_TIMEOUT = 'timeout'
    EXIT_TIMEOUT_WALL = 'wall timeout'
    EXIT_NONZERO_RETURN = 'nonzero return'

    def __init__(self, name=None, temp_dir=None,box_id=None):
        """Initialization.

        file_cacher (FileCacher): an instance of the FileCacher class
            (to interact with FS), if the sandbox needs it.
        name (string|None): name of the sandbox, which might appear in the
            path and in system logs.
        temp_dir (unicode|None): temporary directory to use; if None, use the
            default temporary directory specified in the configuration.

        """
        
        self.name = name if name is not None else "unnamed"
        self.temp_dir = temp_dir if temp_dir is not None else None
        self.cmd_file = "commands.log"
        self.fsize = None
        self.cgroup = False
        self.dirs = []
        self.preserve_env = False
        self.inherit_env = []
        self.set_env = {}
        self.verbosity = 0
        self.max_processes = 1
        if box_id is None:
            self.box_id = IsolateSandbox.next_id % env.max_box 
            IsolateSandbox.next_id = (IsolateSandbox.next_id +1)% env.max_box
        else:
            self.box_id = box_id
        if self.temp_dir is None:
            self.temp_dir = "/var/local/lib/isolate/{}/box".format(self.box_id)


        
        self.secure_folder = str(uuid4()) # secure
        mkdir(self.relative_path(self.secure_folder))
        self.exec_name = 'isolate'
        self._outer_dir = self.temp_dir
        
        # self._home = os.path.join(self._outer_dir, "home")
        
        # self._home_dest = "/tmp"
        # os.mkdir(self._home)
        # os.system("ls {}".format(self._home))
        # logging.debug(self._home)
        # self.allow_writing_all()

        self.exec_name = 'isolate'
        # self.box_exec = self.detect_box_executable()
        # Used for -M - the meta file ends up in the outer directory. The
        # actual filename will be <info_basename>.<execution_number>.
        # self.info_basename = os.path.join(self._outer_dir, "run.log")
        self.log = None
        self.exec_num = -1
        self.cmd_file = os.path.join(self._outer_dir, "commands.log")
        

        self.box_exec = env.ISOLATE
        
        self.info_basename = os.path.join(self._outer_dir, "run.log")
        
        self.log = None
        self.exec_num = -1
        self.cmd_file = os.path.join(self._outer_dir, "commands.log")
        
        logger.debug("Sandbox in `%s' created, using box `%s'.",
                     self.temp_dir, self.box_id)


        self.cgroup = True  # --cg
        self.dirs = []                 # -d
        self.preserve_env = False      # -e
        self.inherit_env = []          # -E
        self.set_env = {}              # -E
        self.fsize = None              # -f
        self.stdin_file = None         # -i
        self.stack_space = None        # -k
        self.address_space = None      # -m
        self.stdout_file = None        # -o
        self.stderr_file = None        # -r
        self.timeout = None            # -t
        self.verbosity = 0             # -v
        self.wallclock_timeout = None  # -w
        self.extra_timeout = None      # -x
        self.chdir = None
        self.cleanup()
        self.initialize_isolate()

    @classmethod
    def __unsafety_execute_command(cls, command):
        '''
        [WARNING !!!]
        This function execute command without sandboxing, this is very dangerous
        This function only use to execute trusted code. 
        Trusted code should only be system's code.
        If you want to execute untrusted code, considering safety_execute function.
        '''
        child_process = subprocess.Popen(command, 
                                        stdin=subprocess.PIPE, 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.PIPE)
        stdout, stderr = child_process.communicate()
        returncode = child_process.returncode
        return returncode, stdout.decode('utf-8'), stderr.decode('utf-8')

    def cleanup(self, delete=False):
        """See Sandbox.cleanup()."""
        # The user isolate assigns within the sandbox might have created
        # subdirectories and files therein, making the user outside the sandbox
        # unable to delete the whole tree. If the caller asked us to delete the
        # sandbox, we first issue a chmod within isolate to make sure that we
        # will be able to delete everything. If not, we leave the files as they
        # are to avoid masking possible problems the admin wanted to debug.

        command = [env.ISOLATE, '--cg', '--box-id={}'.format(self.box_id), '--cleanup']
        logging.info(command)
        returncode, stdout, stderr = self.__unsafety_execute_command(command)
        return returncode, stdout, stderr

    def initialize_isolate(self):
        """Initialize isolate's box."""
        command = [env.ISOLATE, '--cg', '--box-id={}'.format(self.box_id), '--init']
        logging.info(command)
        returncode, stdout, stderr = self.__unsafety_execute_command(command)
        os.system("mkdir {}".format(os.path.join(self.temp_dir,self.secure_folder)))
        return returncode, stdout, stderr

    def build_box_options(self):
        """Translate the options defined in the instance to a string
        that can be postponed to isolate as an arguments list.

        return ([string]): the arguments list as strings.

        """
        res = list()
        if self.box_id is not None:
            res += ["--box-id=%d" % self.box_id]
        if self.cgroup:
            res += ["--cg", "--cg-timing"]
        if self.chdir is not None:
            res += ["--chdir=%s" % self.chdir]
        for src, dest, options in self.dirs:
            s = dest + "=" + src
            if options is not None:
                s += ":" + options
            res += ["--dir=%s" % s]
        if self.preserve_env:
            res += ["--full-env"]
        for var in self.inherit_env:
            res += ["--env=%s" % var]
        for var, value in self.set_env.items():
            res += ["--env=%s=%s" % (var, value)]
        if self.fsize is not None:
            # Isolate wants file size as KiB.
            res += ["--fsize=%d" % (self.fsize // 1024)]
        if self.stdin_file is not None:
            res += ["--stdin=%s" % self.inner_absolute_path(self.stdin_file)]
        if self.stack_space is not None:
            # Isolate wants stack size as KiB.
            res += ["--stack=%d" % (self.stack_space // 1024)]
        if self.address_space is not None:
            # Isolate wants memory size as KiB.
            if self.cgroup:
                res += ["--cg-mem=%d" % (self.address_space // 1024)]
            else:
                res += ["--mem=%d" % (self.address_space // 1024)]
        if self.stdout_file is not None:
            res += ["--stdout=%s" % self.inner_absolute_path(self.stdout_file)]
        if self.max_processes is not None:
            res += ["--processes=%d" % self.max_processes]
        else:
            res += ["--processes"]
        if self.stderr_file is not None:
            res += ["--stderr=%s" % self.inner_absolute_path(self.stderr_file)]
        if self.timeout is not None:
            res += ["--time=%g" % self.timeout]
        res += ["--verbose"] * self.verbosity
        if self.wallclock_timeout is not None:
            res += ["--wall-time=%g" % self.wallclock_timeout]
        if self.extra_timeout is not None:
            res += ["--extra-time=%g" % self.extra_timeout]
        res += ["--meta=%s" % ("%s.%d" % (self.info_basename, self.exec_num))]
        res += ["--run"]
        return res

    def get_stats(self):
        """Return a human-readable string representing execution time
        and memory usage.

        return (string): human-readable stats.

        """
        execution_time = self.get_execution_time()
        if execution_time is not None:
            time_str = "%.3f sec" % (execution_time)
        else:
            time_str = "(time unknown)"
        memory_used = self.get_memory_used()
        if memory_used is not None:
            mem_str = "%.2f MB" % (memory_used / (1024 * 1024))
        else:
            mem_str = "(memory usage unknown)"
        return "[%s - %s]" % (time_str, mem_str)
    def add_mapped_directory(self, src, dest=None, options=None,
                             ignore_if_not_existing=False):
        """Add src to the directory to be mapped inside the sandbox.

        src (str): directory to make visible.
        dest (str|None): if not None, the path where to bind src.
        options (str|None): if not None, isolate's directory rule options.
        ignore_if_not_existing (bool): if True, ignore the mapping when src
            does not exist (instead of having isolate terminate with an
            error).

        """
        if dest is None:
            dest = src
        if ignore_if_not_existing and not os.path.exists(src):
            return
        self.dirs.append((src, dest, options))

    def maybe_add_mapped_directory(self, src, dest=None, options=None):
        """Same as add_mapped_directory, with ignore_if_not_existing."""
        return self.add_mapped_directory(src, dest, options,
                                         ignore_if_not_existing=True)


    def set_multiprocess(self, multiprocess):

        """Set the sandbox to (dis-)allow multiple threads and processes.

        multiprocess (bool): whether to allow multiple thread/processes or not.
        """
        if multiprocess:
            # Max processes is set to 1000 to limit the effect of fork bombs.
            self.max_processes = 1000
        else:
            self.max_processes = 1

    def execute_without_std(self, command, wait=False):
        """Execute the given command in the sandbox using
        subprocess.Popen and discarding standard input, output and
        error. More specifically, the standard input gets closed just
        after the execution has started; standard output and error are
        read until the end, in a way that prevents the execution from
        being blocked because of insufficient buffering.

        command ([string]): executable filename and arguments of the
            command.
        wait (bool): True if this call is blocking, False otherwise

        return (bool|Popen): if the call is blocking, then return True
            if the sandbox didn't report errors (caused by the sandbox
            itself), False otherwise; if the call is not blocking,
            return the Popen object from subprocess.

        """

        popen = self._popen(command, stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            close_fds=True)

        # If the caller wants us to wait for completion, we also avoid
        # std*** to interfere with command. Otherwise we let the
        # caller handle these issues.
        if wait:
            return self.translate_box_exitcode(wait_without_std([popen])[0])
        else:
            return popen

    def translate_box_exitcode(self, exitcode):
        """Translate the sandbox exit code to a boolean sandbox success.

        Isolate emits the following exit codes:
        * 0 -> both sandbox and internal process finished successfully (meta
            file will contain "status:OK" -> return True;
        * 1 -> sandbox finished successfully, but internal process was
            terminated, e.g., due to timeout (meta file will contain
            status:x" with x in (TO, SG, RE)) -> return True;
        * 2 -> sandbox terminated with an error (meta file will contain
            "status:XX") -> return False.

        """
        if exitcode == 0 or exitcode == 1:
            return True
        elif exitcode == 2:
            return False
        else:
            raise SandboxInterfaceException("Sandbox exit status (%d) unknown"
                                            % exitcode)



    def _popen(self, command,
               stdin=None, stdout=None, stderr=None,
               close_fds=True):
        """Execute the given command in the sandbox using
        subprocess.Popen, assigning the corresponding standard file
        descriptors.

        command ([string]): executable filename and arguments of the
            command.
        stdin (int|None): a file descriptor.
        stdout (int|None): a file descriptor.
        stderr (int|None): a file descriptor.
        close_fds (bool): close all file descriptor before executing.

        return (Popen): popen object.

        """
        self.log = None
        self.exec_num += 1
        if not isinstance(command,list): command = [command]
        args = [self.box_exec] + self.build_box_options() + ["--"] + command
        logger.debug("Executing program in sandbox with command: `%s'.",
                     pretty_print_cmdline(args))
        

        with open(self.cmd_file, 'at', encoding="utf-8") as commands:
            commands.write("%s\n" % (pretty_print_cmdline(args)))

        try:
            p = subprocess.Popen(args,
                                 stdin=stdin, stdout=stdout, stderr=stderr,
                                 close_fds=close_fds)
        except OSError:
            logger.critical("Failed to execute program in sandbox "
                            "with command: %s", pretty_print_cmdline(args),
                            exc_info=True)
            raise

        return p

    def _write_empty_run_log(self, index):
        """Write a fake run.log file with no information."""
        info_file = "%s.%d" % (self.info_basename, index)
        with open(info_file, "wt", encoding="utf-8") as f:
            f.write("time:0.000\n")
            f.write("time-wall:0.000\n")
            f.write("max-rss:0\n")
            f.write("cg-mem:0\n")
    def relative_path(self, path):
        """Translate from a relative path inside the sandbox to a system path.

        path (string): relative path of the file inside the sandbox.

        return (string): the absolute path.

        """
        return os.path.join(self.temp_dir, path)   

    def get_file_text(self, path, trunc_len=None):
        """Open a file in the sandbox given its relative path, in text mode.

        Assumes encoding is UTF-8. The caller must handle decoding errors.

        path (str): relative path of the file inside the sandbox.
        trunc_len (int|None): if None, does nothing; otherwise, before
            returning truncate it at the specified length.

        return (file): the file opened in read binary mode.

        """
        logger.debug("Retrieving text file %s from sandbox.", path)
        real_path = self.relative_path(path)
        file_ = open(real_path, "rt", encoding="utf-8")
        if trunc_len is not None:
            file_ = Truncator(file_, trunc_len)
        return file_
    def get_file_to_string(self, path, maxlen=1024):
        """Return the content of a file in the sandbox given its
        relative path.

        path (str): relative path of the file inside the sandbox.
        maxlen (int): maximum number of bytes to read, or None if no
            limit.

        return (string): the content of the file up to maxlen bytes.

        """
        with self.get_file(path) as file_:
            if maxlen is None:
                return file_.read()
            else:
                return file_.read(maxlen)
    def get_file(self, path, trunc_len=None):
        """Open a file in the sandbox given its relative path.

        path (str): relative path of the file inside the sandbox.
        trunc_len (int|None): if None, does nothing; otherwise, before
            returning truncate it at the specified length.

        return (file): the file opened in read binary mode.

        """
        logger.debug("Retrieving file %s from sandbox.", path)
        real_path = self.relative_path(path)
        file_ = open(real_path, "rb")
        if trunc_len is not None:
            file_ = Truncator(file_, trunc_len)
        return file_
    def get_log(self):
        """Read the content of the log file of the sandbox (usually
        run.log.N for some integer N), and set self.log as a dict
        containing the info in the log file (time, memory, status,
        ...).

        """
        # self.log is a dictionary of lists (usually lists of length
        # one).
        self.log = {}
        info_file = "%s.%d" % (self.info_basename, self.exec_num)
        try:
            with self.get_file_text(info_file) as log_file:
                for line in log_file:
                    key, value = line.strip().split(":", 1)
                    if key in self.log:
                        self.log[key].append(value)
                    else:
                        self.log[key] = [value]
        except OSError as error:
            raise OSError("Error while reading execution log file %s. %r" %
                          (info_file, error))

    @with_log
    def get_execution_time(self):
        """Return the time spent in the sandbox, reading the logs if
        necessary.

        return (float): time spent in the sandbox.

        """
        if 'time' in self.log:
            return float(self.log['time'][0])
        return None

    @with_log
    def get_execution_wall_clock_time(self):
        """Return the total time from the start of the sandbox to the
        conclusion of the task, reading the logs if necessary.

        return (float): total time the sandbox was alive.

        """
        if 'time-wall' in self.log:
            return float(self.log['time-wall'][0])
        return None

    @with_log
    def get_memory_used(self):
        """Return the memory used by the sandbox, reading the logs if
        necessary.

        return (int): memory used by the sandbox (in bytes).

        """
        if 'cg-mem' in self.log:
            # Isolate returns memory measurements in KiB.
            return int(self.log['cg-mem'][0]) * 1024
        return None

    @with_log
    def get_killing_signal(self):
        """Return the signal that killed the sandboxed process,
        reading the logs if necessary.

        return (int): offending signal, or 0.

        """
        if 'exitsig' in self.log:
            return int(self.log['exitsig'][0])
        return 0

    @with_log
    def get_exit_code(self):
        """Return the exit code of the sandboxed process, reading the
        logs if necessary.

        return (int): exitcode, or 0.

        """
        if 'exitcode' in self.log:
            return int(self.log['exitcode'][0])
        return 0

    @with_log
    def get_status_list(self):
        """Reads the sandbox log file, and set and return the status
        of the sandbox.

        return (list): list of statuses of the sandbox.

        """
        if 'status' in self.log:
            return self.log['status']
        return []

    def get_exit_status(self):
        """Get the list of statuses of the sandbox and return the most
        important one.

        return (string): the main reason why the sandbox terminated.

        """
        status_list = self.get_status_list()
        if 'XX' in status_list:
            return self.EXIT_SANDBOX_ERROR
        elif 'TO' in status_list:
            if 'message' in self.log and 'wall' in self.log['message'][0]:
                return self.EXIT_TIMEOUT_WALL
            else:
                return self.EXIT_TIMEOUT
        elif 'SG' in status_list:
            return self.EXIT_SIGNAL
        elif 'RE' in status_list:
            return self.EXIT_NONZERO_RETURN
        # OK status is not reported in the log file, it's implicit.
        return self.EXIT_OK

    def get_stderr(self):
        line = []
        if os.path.isfile(os.path.join(self.temp_dir,self.stderr_file)):
            with open(os.path.join(self.temp_dir,self.stderr_file),"r") as f:
                line = f.read()
        return line

    def get_human_exit_description(self):
        """Get the status of the sandbox and return a human-readable
        string describing it.

        return (string): human-readable explaination of why the
                         sandbox terminated.

        """
        status = self.get_exit_status()
        if status == self.EXIT_OK:
            return "Execution successfully finished (with exit code %d)" % \
                self.get_exit_code()
        elif status == self.EXIT_SANDBOX_ERROR:
            return "Execution failed because of sandbox error"
        elif status == self.EXIT_TIMEOUT:
            return "Execution timed out"
        elif status == self.EXIT_TIMEOUT_WALL:
            return "Execution timed out (wall clock limit exceeded)"
        elif status == self.EXIT_SIGNAL:
            return "Execution killed with signal %s" % \
                self.get_killing_signal()
        elif status == self.EXIT_NONZERO_RETURN:
            return "Execution failed because the return code was nonzero"

    def inner_absolute_path(self, path):
        """Translate from a relative path inside the sandbox to an
        absolute path inside the sandbox.

        path (string): relative path of the file inside the sandbox.

        return (string): the absolute path of the file inside the sandbox.

        """
        return path
    def get_root_path(self):return self.temp_dir


    def create_file(self, path, executable=False,secure=False):
        """Create an empty file in the sandbox and open it in write
        binary mode.

        path (string): relative path of the file inside the sandbox.
        executable (bool): to set permissions.

        return (file): the file opened in write binary mode.

        """
        if executable:
            logger.debug("Creating executable file %s in sandbox.", path)
        else:
            logger.debug("Creating plain file %s in sandbox.", path)
        real_path = self.relative_path(path)
        if secure:
            real_path = os.path.join(self.relative_path(self.secure_folder),path)
        try:
            file_fd = os.open(real_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            file_ = open(file_fd, "wb")
        except OSError as e:
            logger.error("Failed create file %s in sandbox. Unable to "
                         "evalulate this submission. This may be due to "
                         "cheating. %s", real_path, e, exc_info=True)
            raise
        mod = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR
        if executable:
            mod |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(real_path, mod)
        return file_

    def allow_chmod(self,path):
        path = self.relative_path(path)
        mod = stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH | stat.S_IWUSR
        
        mod |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(path, mod)
        

    def create_folder(self,path,secure=False):
        real_path = self.relative_path(path) 
        if secure :
            real_path = self.relative_path(os.path.join(self.secure_folder,path))
        if os.path.exists(real_path):
            logger.debug("file exits %s" % real_path)
        else:
            shutil.os.mkdir(real_path)

    def create_file_from_storage(self,path, digest, executable=False,secure=False):
        real_path = os.path.join(self.relative_path(self.secure_folder),path)
        if not secure:real_path = self.relative_path(path)
        if os.path.isdir(digest):
            shutil.copytree(digest, real_path) 
        else:
            shutil.copyfile(digest,real_path)
    def create_file_from_string(self, path, content, executable=False,secure=False):
        """Write some data to a file in the sandbox.

        path (string): relative path of the file inside the sandbox.
        content (string): what to write in the file.
        executable (bool): to set permissions.

        """
        
        self.create_file(path, executable,secure=secure)
        real_path = os.path.join(self.relative_path(self.secure_folder),path)
        if not secure:real_path = self.relative_path(path)
        with open(real_path,'w') as dest_fobj:
            dest_fobj.write(content)

    def get_dir(self,path,secure=False):
        real_path = os.path.join(self.secure_folder,path) if secure else path
        real_path = self.relative_path(real_path)
        # secure_path = os.path.join(self.sandbox.temp_dir, self._mapanotation_[path])
        # logging.debug(secure_path)
        if os.path.isdir(real_path):
            return [os.path.join(path,f) for f in os.listdir(real_path)]
        return []


