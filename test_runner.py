from datetime import datetime
from dotenv import load_dotenv
import json
import os
import shlex
import subprocess
import sys

from tests.APEL.gridJobTest import run_test as grid_job_test
from tests.FTS.certificate.skaTest import run_test as fts_cert_ska_test
from tests.FTS.certificate.testTest import run_test as fts_cert_test_test
from tests.FTS.certificate.wlcgTest import run_test as fts_cert_wlcg_test
from tests.FTS.token.skaTest import run_test as fts_token_ska_test
from tests.FTS.token.testTest import run_test as fts_token_test_test
from tests.FTS.token.wlcgTest import run_test as fts_token_wlcg_test

load_dotenv()

tests = [
    grid_job_test,
    fts_cert_ska_test,
    fts_cert_test_test,
    fts_cert_wlcg_test,
    fts_token_ska_test,
    fts_token_test_test,
    fts_token_wlcg_test
]

results = []

# voms proxy creation
command = "voms-proxy-init --voms dteam"
vomsProxyPassword = os.getenv("vomsproxypassword")

result = subprocess.run(
    shlex.split(command),
    input=vomsProxyPassword + "\n",
    capture_output=True,
    text=True
)

# exit program if proxy creation fails, as all tests will fail because of it
if result.returncode != 0:
    print(result.stdout + result.stderr)
    sys.exit()

# run all tests and append results to list
for test in tests:
    results.append(test())

# create test output from results list
output = {
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "results": results
}

# append test results to log file
with open("/var/log/fed-services-e2e/test_results_log.jsonl", "a") as f:
    json.dump(output, f)
    f.write("\n")

# opensearch api ingestion logic
