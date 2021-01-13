



try:

    from ..job.OutputOnly import OutputOnly

except:
    from job.OutputOnly import OutputOnly
    from config import env





contestant_source = []
with open("/opt/test/source_code_for_testing/par.cpp","r") as f:
    contestant_source = f.read()



job_description = {
    "id":1,
    "multiprocess":False,
    "time":3.,
    "contestant_source":contestant_source,
    "contestant_lang":"cpp",
    "checker":"/opt/test/problems_test/4/checker.cpp",
    "checker_lang":"cpp",
    "inputs":"/opt/test/problems_test/4/inputs",
    "outputs":"/opt/test/problems_test/4/outputs",
    "type":"ioi",
    "sess":"submit",
}

wo = OutputOnly(job_description)
# wo.prepare_file()
# wo.compiler()
wo.run()
wo.eval_status()
# wo.sandbox.cleanup()
# wo.sandbox.cleanup()