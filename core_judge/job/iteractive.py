



import logging
import os
import os,sys,inspect
from .base import JobBase
import tempfile
try:
    from ..sandbox.sandbox import IsolateSandbox as Sandbox
    from ..languageall import get_language,filename_to_language
    from ..steps.compilation import compilation_step
    from ..config import env
    from ..steps.evaluation import evaluation_step_after_run,evaluation_step_before_run,evaluation_step
except:
    from sandbox.sandbox import IsolateSandbox as Sandbox
    from languageall import get_language,filename_to_language
    from steps.compilation import compilation_step
    from config import env
    from steps.evaluation import evaluation_step_after_run,evaluation_step_before_run,evaluation_step
try:
    from ..sandbox.sandbox import IsolateSandbox ,wait_without_std
except:
    from sandbox.sandbox import IsolateSandbox,wait_without_std
import os



class Iteractive(JobBase):
    def __init__(self, jobdescription):
        self.jobdescription = jobdescription
        # self.sandbox = IsolateSandbox()
        self.sandbox = IsolateSandbox(box_id=jobdescription.get("id",None))
        # self.compiler = CompilationJob(self.sandbox)
        logging.debug(jobdescription["time"])
        self.multiprocess = self.jobdescription.get("multiprocess",1000)

        
        # self.multiprocess = 1000
        self.time_limit = self.jobdescription.get("time",1.)
        self.memory_limit= self.jobdescription.get("mem",None)
        self.dirs_map = self.jobdescription.get("dirs_map",None)
        if 'checker_lang' not in self.jobdescription.keys():
            self.jobdescription['checker_lang'] = self.jobdescription['checker'].split(".")[-1]
        # contestant_source = self.jobdescription["contestant_source"]
        
        self.lang_source = self.jobdescription["contestant_lang"]

        self.file_source =os.path.join(self.sandbox.temp_dir,"contestant_source" + "."+self.lang_source)

        self.path_contestant = "contestant_source." + jobdescription['contestant_lang']

    def prepare_file(self):

        self.sandbox.create_file_from_string(self.path_contestant,self.jobdescription['contestant_source'],secure=False)
        self.update_status(log="copy file contestant to sandbox")
        # prepare inputs

        self.sandbox.create_file_from_storage('inputs',self.jobdescription['inputs'],secure=True)
        self.sandbox.create_file_from_storage('outputs',self.jobdescription['outputs'],secure=True)
        # prepare checkers

        self.update_status(log="copy file in/out to sandbox")
        self.sandbox.create_file_from_storage('checker.' + self.jobdescription['checker_lang'],self.jobdescription['checker'],secure=True)
        self.sandbox.create_file_from_storage("testlib.h",env.TESTLIB,secure=True)
        self.update_status(log="copy file checker to sandbox")

        self.sandbox.create_file_from_storage("iteractor." +self.jobdescription['iteractor_lang'],self.jobdescription['iteractor'],secure=True)
        # selfl.sandbox.create_file_from_storage("testlib.h",env.TESTLIB,secure=True)

        self.update_status(log="copy file iteractor to sandbox")


        self.fifo_dir = [self.sandbox.temp_dir]

        # can run more than one code_participant
        self.fifo_user_to_manager = [
            os.path.join(self.fifo_dir[i], "u%d_to_m" % i) for i in [0]]
        self.fifo_manager_to_user = [
            os.path.join(self.fifo_dir[i], "m_to_u%d" % i) for i in [0]]

        
        os.mkfifo(self.fifo_user_to_manager[0])
        os.mkfifo(self.fifo_manager_to_user[0])
            # os.system("touch %s" %fifo_user_to_manager[i])
            # os.system("touch %s" %fifo_manager_to_user[i])
            # logging.debug(fifo_manager_to_user[i])
        os.chmod(self.fifo_dir[0], 0o755)
        os.chmod(self.fifo_user_to_manager[0], 0o6666)
        os.chmod(self.fifo_manager_to_user[0], 0o6666)
        self.sandbox_fifo_dir = ["" for i in [0]]

        self.sandbox_fifo_user_to_manager = [
            os.path.join(self.sandbox_fifo_dir[i], "u%d_to_m" % i) for i in [0]]

        self.sandbox_fifo_manager_to_user = [
            os.path.join(self.sandbox_fifo_dir[i], "m_to_u%d" % i) for i in [0]]

        self.update_status(log="create done fifo file")
        

    def compiler(self):
        # logging.debug("compiler contestant")
        # self.update_status()
        source_filename = ['contestant_source.' + self.lang_source]
        executable_filename = "contestant_source"
        lang = filename_to_language(self.path_contestant)

        commands =lang.get_compilation_commands(source_filename,executable_filename)

        status = compilation_step(self.sandbox,commands)

        if status[0] is not True or status[1] is not True:
            # logging.debug("contestant compiler fail")
            self.update_status(log="contestant compiler fail")
            return status
        

        # todo compiled default iteractor
        self.update_status(log=status[-1])
        source_filename = [os.path.join(self.sandbox.secure_folder,'iteractor.cpp')]
        executable_filename=os.path.join(self.sandbox.secure_folder,"iteractor")
        lang = filename_to_language("."+self.jobdescription['iteractor_lang'])
        commands = lang.get_compilation_commands(source_filename,executable_filename)
        status = compilation_step(self.sandbox,commands)

        if status[0] is not True or status[1] is not True:
            self.update_status(log="iteractor compiler fail")
            return status
        
        if self.jobdescription.get("checker_compiled",None) is not None:
            self.sandbox.create_file_from_storage('checker',self.jobdescription['checker_compiled'],secure=True)
            self.sandbox.allow_chmod(os.path.join(self.sandbox.secure_folder,'checker'))

        return status
        # compiler ton nhieu thoi gian trong th iteractive chung ta ko can compile cai checker som

    
 

    
    def run_per_test(self,idx):
        

        jury_input = os.path.join(self.sandbox.secure_folder,'inputs/{}.in'.format(idx))
        
        # jury_output = os.path.join(self.sandbox.secure_folder,'outputs/{}.out'.format(idx))
        output_iteractor = '{}.out'.format(idx)

        manager_command = ["./"+os.path.join(self.sandbox.secure_folder,'iteractor')] # iteractir fifo user->ma : ma->user
        
        manager_command = manager_command  + self.sandbox_fifo_user_to_manager + self.sandbox_fifo_manager_to_user

        manager_time_limit = max(1 * (1 + self.time_limit),
                                 env.trusted_sandbox_max_time_s)
        

        # run manager
        manager = evaluation_step_before_run(
            self.sandbox,
            command=manager_command,
            time_limit= manager_time_limit,
            # memory_limit= env.max_file_size * 1024,
            # dirs_map=dict((self.fifo_dir[0], (self.sandbox_fifo_dir[0], "rw"))
            #               for i in [0]),
            # writable_files=[self.OUTPUT_FILENAME],
            stdin_redirect=jury_input,
            stdout_redirect=output_iteractor,
            multiprocess=self.multiprocess,wait=False)

        
        user_command = ["./contestant_source"]
        user_command = user_command + self.sandbox_fifo_manager_to_user + self.sandbox_fifo_user_to_manager  
        stdint_redirect = self.sandbox_fifo_manager_to_user[0]
        stdout_redirect = self.sandbox_fifo_user_to_manager[0]

        user =evaluation_step_before_run(
            self.sandbox,command=user_command,time_limit=self.time_limit,
            memory_limit=self.memory_limit,
            # dirs_map={self.fifo_dir[0]: (self.sandbox_fifo_dir[0], "rw")},
            stdin_redirect=stdint_redirect,
            stdout_redirect=stdout_redirect,
            multiprocess=self.multiprocess,wait=False
            )

        # communication
        wait_without_std([user,manager])

        status= evaluation_step_after_run(self.sandbox)

        if status[0] is not True or status[1] is not True:
            self.update_status(log=status[-1])
            return False

        

        if idx == 1 and self.jobdescription.get("checker_compiled",None) is None:
            # compilder_checker
            source_filename=[os.path.join(self.sandbox.secure_folder,'checker') + ".cpp"]
            executable_filename=os.path.join(self.sandbox.secure_folder,'checker')
            lang = filename_to_language("." +self.jobdescription['checker_lang'])
            logging.debug(lang)
            logging.debug(source_filename)
            logging.debug(executable_filename)
            commands = lang.get_compilation_commands(source_filename,executable_filename)
            logging.debug(commands)
            status = compilation_step(self.sandbox,commands)
            if status[0] is not True or status[1] is not True:
                 # logging.debug("contestant compiler fail")
                logging.debug("checker compiler fail")
                return False


        logging.debug("checker done")
        checker_exec = os.path.join(self.sandbox.secure_folder,"checker")

        jury_output = os.path.join(self.sandbox.secure_folder,"outputs/{}.out".format(idx))
        commands = [[checker_exec] +[jury_input] + [output_iteractor]+[jury_output] ]

        status_step = evaluation_step(self.sandbox, commands,self.time_limit,self.memory_limit,self.dirs_map,
            stdin_redirect=None, stdout_redirect=None,multiprocess=self.multiprocess)
        # self.update_status(log=status_step)
        if status_step[1] != True:
            log_checker = self.sandbox.get_stderr()
            self.update_status(log=log_checker)
            # self.score.step(idx,0)
            return False
        # self.update_status(log="here")
        self.update_status(log=status_step[2])
        return True

    def update_status(self,log=""):
        logging.debug(log)
        
    def run(self):
        # prepare file
        try:
            self.prepare_file()
        except:
            self.update_status(log="file storage erros")
            return None

        # compiler
        status = self.compiler()
        if status[0] is not True or status[1] is not True:
            self.update_status(log="compiler erros")
            return status
        
        # run pertest 


        inputs = self.sandbox.get_dir("inputs",secure=True)
        
        for idx,item in enumerate(inputs,1):
            if not self.run_per_test(idx):return
