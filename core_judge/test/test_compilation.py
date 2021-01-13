




try:
    from ..sandbox.sandbox import IsolateSandbox as Sandbox
    from ..languageall import get_language,filename_to_language
    from ..steps.compilation import compilation_step
except:
    from sandbox.sandbox import IsolateSandbox as Sandbox
    from languageall import get_language,filename_to_language
    from steps.compilation import compilation_step



sandbox = Sandbox()


contestant_source = []
with open("/opt/test/source_code_for_testing/par.cpp","r") as f:
    contestant_source = f.read()

from config import env
job_description = {
    "multiprocess":False,
    "time":1.,
    "contestant_source":contestant_source,
    "contestant_lang":"cpp",
    "checker":"/opt/test/problems_test/4/checker.cpp",
    "checker_lang":"cpp",
    "inputs":"/opt/test/problems_test/4/inputs",
    "outputs":"/opt/test/problems_test/4/outputs",
    "type":"ioi",
    "sess":"submit",
}
source_checker = ""
# with open(job_description['checker'],'')
path_contestant = "contestant." + job_description['contestant_lang']

sandbox.create_file_from_string(path_contestant,job_description['contestant_source'],secure=False)

sandbox.create_file_from_storage('checker.' + job_description['checker_lang'],job_description['checker'],secure=True)
sandbox.create_file_from_storage("testlib.h",env.TESTLIB,secure=True)
sandbox.create_file_from_storage('inputs',job_description['inputs'],secure=True)
sandbox.create_file_from_storage('outputs',job_description['outputs'],secure=True)

source_filename = ['contestant.cpp']
executable_filename = "contestant"
import os
executable_filename_checker=os.path.join(sandbox.secure_folder,"checker")
source_checker_filename = os.path.join(sandbox.secure_folder,"checker.cpp")
lang = filename_to_language(path_contestant)
commands =lang.get_compilation_commands(source_filename,executable_filename) 
commands = commands +  lang.get_compilation_commands([source_checker_filename],executable_filename_checker)

print(commands)
status = compilation_step(sandbox,commands)
print(status)
# return status
sandbox.cleanup()
# 

