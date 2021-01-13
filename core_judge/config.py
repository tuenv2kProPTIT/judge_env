
class Env(object):
    def __init__(self):
        self.use_cgroups = True
        self.temp_dir = '/tmp'
        self.backdoor = False
        self.file_log_debug = False
        self.stream_log_detailed = False



        # Worker.
        self.keep_sandbox = True
        self.use_cgroups = True
        self.sandbox_implementation = 'isolate'

        # Sandbox.
        # Max size of each writable file during an evaluation step, in KiB.
        self.max_file_size = 256 * 1024  # 1 GiB
        # Max processes, CPU time (s), memory (KiB) for compilation runs.
        self.compilation_sandbox_max_processes = 1000
        self.compilation_sandbox_max_time_s = 10.0
        self.compilation_sandbox_max_memory_kib = 512 * 1024  # 512 MiB
        # Max processes, CPU time (s), memory (KiB) for trusted runs.
        self.trusted_sandbox_max_processes = 1000
        self.trusted_sandbox_max_time_s = 10.0
        self.trusted_sandbox_max_memory_kib = 2 * 1024 * 1024  # 4 GiB

env = Env()

# Lấy địa chỉ đường dẫn các trình biên dịch, thực thi


import os
import logging

env.level_logging = logging.DEBUG

logging.basicConfig(level=env.level_logging)
# Lấy địa chỉ đường dẫn các trình biên dịch, thực thi

# C/C++
try:
    env.GCC_PATH = os.environ['GCC_PATH']
    env.GPP_PATH = os.environ['GPP_PATH']
    # env.log_level = os.environ['']
except:
    env.GCC_PATH = "/usr/bin/x86_64-linux-gnu-gcc-7"
    env.GPP_PATH ="/usr/bin/x86_64-linux-gnu-g++-7"

# env.GPP_PATH = 
# Python
# env.PY3_PATH = os.environ['PY3_PATH']

# Java
# JAVA_PATH = os.environ['JAVA_PATH']
# JAVAC_PATH = os.environ['JAVAC_PATH']

# Isolate Sandbox
env.ISOLATE = "/usr/local/bin/isolate"
env.max_box=1000
# Testlib
env.TESTLIB = os.path.join(os.path.dirname(__file__), "testlib", "testlib.h")

# Check env

# def check_env():
#     logging.info("Checking Environment ...")
#     if not os.path.isfile(GCC_PATH):
#         raise EnvironmentError("C Compiler Not Found")
#     if not os.path.isfile(GPP_PATH):
#         raise EnvironmentError("C++ Compiler Not Found")
#     if not os.path.isfile(PY3_PATH):
#         raise EnvironmentError("Python3 Interpreter Not Found")
#     if not os.path.isfile(JAVA_PATH):
#         raise EnvironmentError("Java Virtual Machine (JVM) Not Found")
#     if not os.path.isfile(JAVAC_PATH):
#         raise EnvironmentError("Java Compiler Not Found")
#     if not os.path.isfile(ISOLATE):
#         raise EnvironmentError("Isolate Sandbox Not Found")
#     logging.info("Checking Environment Done")

# check_env()

