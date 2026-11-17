from datetime import datetime, timezone
import json
import shlex
import subprocess

import settings
from tests.APEL.gridJobTest import run_test as grid_job_test
from tests.FTS.certificate.testTest import run_test as fts_cert_test_test
from tests.FTS.certificate.wlcgTest import run_test as fts_cert_wlcg_test
from tests.FTS.token.skaTest import run_test as fts_token_ska_test

# Create the voms proxy required for grid jobs and FTS certificate transfers.
command = "voms-proxy-init --voms dteam"
vomsProxyPassword = settings.VOMS_PROXY_PASSWORD

result = subprocess.run(
    shlex.split(command),
    input=vomsProxyPassword + "\n",
    capture_output=True,
    text=True
)

# Create output dictionary
output = {
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
}

# If the VOMS proxy creation fails, append an error message to the test results list.
if result.returncode != 0:
    output["runningError"] = ("VOMS Proxy creation fail: " + result.stdout + result.stderr)

# Run the tests, storing their output straight into a dictionary.
output["ftsCertTest"] = fts_cert_test_test()
output["ftsCertWlcg"] = fts_cert_wlcg_test()
output["ftsTokenSka"] = fts_token_ska_test()
output["apelGridJob"] = grid_job_test()

# Append the output dictionary to the test results log file.
# jsonl is used over json so that the Filebeat parser for OpenSearch can consider each line
# of the log file as a different log entry, removing the need for multi-line parsing.
with open("/var/log/fed-services-e2e/test_results_log.jsonl", "a") as f:
    json.dump(output, f)
    f.write("\n")
