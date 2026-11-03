from datetime import datetime, timezone
import os
import shlex
import subprocess

from dotenv import load_dotenv

from resources.ftsTransferResults import get_job_id, get_test_result
from resources.tokenGenerator import generate_token

def run_test():
    # Prepare submissionResult dictionary, in case token generation fails
    submissionResult = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "duration": 0,
        "status": "",
        "return_code": "",
        "output": "",
        "error": "",
    }

    load_dotenv()

    # Generate a token with SKA params
    token = generate_token(
        token_endpoint="https://ska-iam.stfc.ac.uk/token",
        client_id=os.getenv("skaClientId"),
        client_secret=os.getenv("skaClientSecret")
    )

    # Check if token generation failed. If so return submissionResult dictionary before test exection,
    # containing the token generation error message.
    if not token or "OIDC" in token:
        submissionResult["status"] = "FAIL"
        submissionResult["output"] = "Failed to generate a token"
        submissionResult["error"] = token
        return submissionResult

    endpoint = "https://fts-ska01.scd.rl.ac.uk:8446"
    sourceFile = "davs://xrootd-01.swesrc.chalmers.se:1094/data/src/ops_tests/service_tests/rowane2etest.txt"
    destFile = "davs://rucio.espsrc.iaa.csic.es:443/disk/ops_tests/service_tests/rowane2etest.txt"

    # Token generation succeeded - attempt transfer
    start = datetime.now()

    # Run token transfer to ska instance.
    # By using -o flag (overwrite file), we can always use the same source and destination files.
    command = (
        f"fts-rest-transfer-submit "
        f"--fts-access-token {token} "
        f"--src-access-token {token} "
        f"--dst-access-token {token} "
        f"-s {endpoint} "
        f"{sourceFile} {destFile} -o"
    )
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)

    end = datetime.now()

    # Amend test result dictionary with correct test results
    submissionResult["duration"] = str(end - start)
    submissionResult["status"] = "PASS" if result.returncode == 0 else "FAIL"
    submissionResult["return_code"] = result.returncode
    submissionResult["output"] = result.stdout
    submissionResult["error"] = result.stderr

    # Dictionary containting information to return
    retDict = {
        "test": "fts token transfer ska endpoint",
        "submission": submissionResult
    }

    # If submission succeeded, retrieve the result of the transfer and return that as well
    jobID = get_job_id(result.stdout)
    if jobID is not None:
        transferResult = get_test_result(
            endpoint=endpoint,
            jobID=jobID,
            token=token
        )

        retDict["transfer"] = transferResult

    return retDict
