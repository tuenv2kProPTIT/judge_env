


import logging
import os
import os,sys,inspect
from .base import JobBase
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
import os,shutil



class Validator(JobBase):
    def __init__(self, jobdescription):
        self.jobdescription = jobdescription
        self.sandbox = IsolateSandbox(box_id=jobdescription.get("id",None))
        # self.compiler = CompilationJob(self.sandbox)
        logging.debug(jobdescription["time"])
        self.multiprocess = self.jobdescription.get("multiprocess",None)
        self.time_limit = self.jobdescription.get("time",1.)
        self.memory_limit= self.jobdescription.get("mem",None)
        self.dirs_map = self.jobdescription.get("dirs_map",None)
        if 'checker_lang' not in self.jobdescription.keys():
            self.jobdescription['checker_lang'] = self.jobdescription['checker'].split(".")[-1]
        # jury_source = self.jobdescription["jury_source"]
        
        self.lang_source = self.jobdescription["jury_lang"]

        self.file_source =os.path.join(self.sandbox.temp_dir,"jury_source" + "."+self.lang_source)

        self.path_contestant = "jury_source." + jobdescription['jury_lang']

    def prepare_file(self):
        self.sandbox.create_file_from_string(self.path_contestant,self.jobdescription['jury_source'],secure=False)
        self.update_status(log="copy file contestant to sandbox")
        # prepare inputs

        self.sandbox.create_file_from_storage('inputs',self.jobdescription['inputs'],secure=True)
        
        # self.sandbox.create_file_from_storage('outputs',self.jobdescription['outputs'],secure=True)
        # prepare checkers

        self.update_status(log="copy file in/out to sandbox")
        self.sandbox.create_file_from_storage('checker.' + self.jobdescription['checker_lang'],self.jobdescription['checker'],secure=True)
        self.sandbox.create_file_from_storage("testlib.h",env.TESTLIB,secure=True)
        self.update_status(log="copy file checker to sandbox")

    def compiler(self):

        logging.debug("compiler contestant")

        source_filename = ['jury_source.' + self.lang_source]
        executable_filename = "jury_source"
        lang = filename_to_language(self.path_contestant)

        commands =lang.get_compilation_commands(source_filename,executable_filename)
# print(commands)
        status = compilation_step(self.sandbox,commands)
        if status[0] is not True or status[1] is not True:
            # logging.debug("contestant compiler fail")
            self.update_status(log=status[-1])
            return status
        # self.update_status(log="contestant compiler succes")
        self.update_status(log= status[-1])
        source_filename=[os.path.join(self.sandbox.secure_folder,'checker') + "." + self.jobdescription['checker_lang']]
        executable_filename=os.path.join(self.sandbox.secure_folder,'checker')
        lang = filename_to_language("." + self.jobdescription['checker_lang'])
        commands = lang.get_compilation_commands(source_filename,executable_filename)
        status = compilation_step(self.sandbox,commands)
        if status[0] is not True or status[1] is not True:
            # logging.debug("contestant compiler fail")
            self.update_status(log="checker compiler fail")
        self.update_status(log= status[-1])
        return status
    
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
            self.update_status(log=status[-1])
            return status
        
        # run pertest 


        inputs = self.sandbox.get_dir("inputs",secure=True)
        
        for idx,item in enumerate(inputs,1):
            if not self.run_per_test(idx):return


    def run_per_test(self,idx):

        commands = ["jury_source"]
        stdin_redirect="inputs" 
        stdin_redirect = os.path.join(stdin_redirect,"{}.in".format(idx))
        stdin_redirect = os.path.join(self.sandbox.secure_folder,stdin_redirect)
        # stdout_redirect = "{}.out".format(idx)

        jury_output="outputs"
        self.sandbox.create_folder(jury_output,secure=True)
        jury_output = os.path.join(jury_output,"{}.out".format(idx))
        jury_output = os.path.join(self.sandbox.secure_folder,jury_output)

        processes=evaluation_step_before_run(self.sandbox,commands,self.time_limit,memory_limit= self.memory_limit,dirs_map=self.dirs_map,
                    stdin_redirect=stdin_redirect,stdout_redirect= jury_output,multiprocess=self.multiprocess,wait=False)

        wait_without_std([processes])

        status_step= \
            evaluation_step_after_run(self.sandbox)
            
        # status_step = evaluation_step(self.sandbox, commands,self.time_limit,self.memory_limit,self.dirs_map,
        #         stdin_redirect, stdout_redirect,multiprocess=self.multiprocess)

        if status_step[1] != True:
            # self.score.step(idx,0)
            self.update_status(log=status_step[2])
            return False
        
        
        self.update_status(log=status_step[2])
        # self.score.step(idx,1)
        return True

    def update_status(self,log=""):
        logging.debug(log)

    def eval_status(self):
        # copy file checker da compiler 
        # copy file outputs
        checker = self.sandbox.relative_path(os.path.join(self.sandbox.secure_folder,'checker'))
        
        copy_checker_to = self.jobdescription.get("checker_compiled",None)

        if copy_checker_to is not None:
            if os.path.exists(copy_checker_to):
                logging.debug("re write file %s" % copy_checker_to)
            shutil.copyfile(checker,copy_checker_to)
            # shutil.copy2
            logging.debug("copy file checker to %s" % copy_checker_to)
        ouputs = self.sandbox.relative_path(os.path.join(self.sandbox.secure_folder,'outputs'))

        copy_outputs_to = self.jobdescription.get("outputs",None)

        if copy_outputs_to is not None:
            if os.path.isdir(copy_outputs_to):
                logging.debug("can't copy to exits folder %s" %copy_outputs_to)
            else:
                shutil.copytree(ouputs,copy_outputs_to)
                self.update_status(log="copy file outputs to %s" % ouputs)
        self.update_status(log="done")
        super().eval_status()        


