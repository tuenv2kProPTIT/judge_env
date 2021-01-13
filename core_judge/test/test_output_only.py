try:

    from ..job.OutputOnly import OutputOnly

except:
    from job.OutputOnly import OutputOnly
    from config import env

contestant_source = []
with open("/opt/test/problems_test/6/solution.cpp","r") as f:
    contestant_source = f.read()



job_description = {
    "id":0,
    "multiprocess":False,
    "time":0.5,
    "contestant_source":contestant_source,
    "contestant_lang":"cpp",
    "checker":"/opt/test/problems_test/6/checker.cpp",
    "checker_lang":"cpp",
    "checker_compiled":"/opt/test/problems_test/6/checker",
    "inputs":"/opt/test/problems_test/6/inputs",
    "outputs":"/opt/test/problems_test/6/outputs",
    "type":"ioi",
    "sess":"submit",
}





wo = OutputOnly(job_description)
# wo.prepare_file()
# wo.compiler()
wo.run()
wo.eval_status()
# wo.sandbox.cleanup()