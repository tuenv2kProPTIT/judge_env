
Judge Test Proptit

REFERENCES:

    IOI-ISOLATE: [ISOLATE](https://github.com/ioi/isolate)

    CMS-DEV : [CMS-DEV](https://cms-dev.github.io/)

---

FEATURE:

1. OUTPUT_INPUT_STANDART_JUDGE
2. ITERACTIVE_JUDGE
3. VALIDATOR_JUDGE
4. CHECKER WITH TESTLIB
[ISOLATE](https://github.com/ioi/isolate)

---

docker-compose up -d --build.

inside docker run test_all.py 

test in folder /core_judge/test

---

TODO :

1. Add score calculator.
2. ADD feature jobdescription files with string not path file.( for save problems with sql...).
3. ADD worker for Job.
4. Separate two SANDBOX for iteractive to check time_limit for manager and user. Or change sandbox to get stderr separate with different stderr file default.
5. ADD api with fastAPI or Flask. 