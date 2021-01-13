






try:

    from ..job.OutputOnly import OutputOnly
    from ..job.validator import Validator

except:
    from job.OutputOnly import OutputOnly
    from job.validator import Validator
    from config import env





contestant_source = []
with open("/opt/test/problems_test/6/solution.cpp","r") as f:
    contestant_source = f.read()



job_description = {
    "id":1,
    "multiprocess":False,
    "time":3.,
    
    "jury_source":contestant_source,
    "jury_lang":"cpp",
    
    "checker":"/opt/test/problems_test/6/checker.cpp",
    "checker_lang":"cpp",
    "checker_compiled":"/opt/test/problems_test/6/checker",
    "inputs":"/opt/test/problems_test/6/inputs",
    "outputs":"/opt/test/problems_test/6/outputs",

    "type":"ioi",
    "sess":"submit",
}

wo = Validator(job_description)
# wo.prepare_file()
# wo.compiler()
# wo.prepare_file()
wo.run()
# wo.compiler()
wo.eval_status()
# wo.sandbox.cleanup()
# wo.sandbox.cleanup()