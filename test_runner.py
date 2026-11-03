from datetime import datetime, timezone
import json
import os
import shlex
import subprocess

from dotenv import load_dotenv

from tests.APEL.gridJobTest import run_test as grid_job_test
from tests.FTS.certificate.testTest import run_test as fts_cert_test_test
from tests.FTS.certificate.wlcgTest import run_test as fts_cert_wlcg_test
from tests.FTS.token.skaTest import run_test as fts_token_ska_test

load_dotenv()

tests = [
    grid_job_test,
    fts_cert_test_test,
    fts_cert_wlcg_test,
    fts_token_ska_test,
]

results = []

# Create the voms proxy required for grid jobs and FTS certificate transfers.
command = "voms-proxy-init --voms dteam"
vomsProxyPassword = os.getenv("vomsproxypassword")

result = subprocess.run(
    shlex.split(command),
    input=vomsProxyPassword + "\n",
    capture_output=True,
    text=True
)

# If the VOMS proxy creation fails, append an error message to the test results list.
if result.returncode != 0:
    results.append("VOMS Proxy creation fail: " + result.stdout + result.stderr)

# run all tests and append results to list
for test in tests:
    results.append(test())

# Create the output dictionary from the list of test results.
output = {
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    "results": results
}

# Append the output dictionary to the test results log file.
# jsonl is used over json so that the Filebeat parser for OpenSearch can consider each line
# of the log file as a different log entry, removing the need for multi-line parsing.
with open("/var/log/fed-services-e2e/test_results_log.jsonl", "a") as f:
    json.dump(output, f)
    f.write("\n")
