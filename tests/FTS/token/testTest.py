from datetime import datetime, timezone
from dotenv import load_dotenv
import os
import shlex
import subprocess

from resources.ftsTransferResults import get_job_id, get_test_result
from resources.tokenGenerator import generate_token

def run_test():
    # Prepare submissionResult dictionary, in case token generation fails
    submissionResult = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "duration": 0,
        "command": "",
        "status": "",
        "return_code": "",
        "output": "",
        "error": "",
    }

    load_dotenv()

    # Generate a token with iris params
    token = generate_token(
        token_endpoint="https://iris-iam.stfc.ac.uk/token",
        client_id=os.getenv("irisClientId"),
        client_secret=os.getenv("irisClientSecret")
    )

    # Check if token generation failed. If so return submissionResult dictionary before test exection,
    # containing the token generation error message.
    if not token or "OIDC" in token:
        submissionResult["status"] = "FAIL"
        submissionResult["output"] = "Failed to generate a token"
        submissionResult["error"] = token
        return submissionResult

    endpoint = "https://fts3-test.gridpp.rl.ac.uk:8446"

    # Token generation succeeded - attempt transfer
    start = datetime.now()

    # Run token transfer to ska instance
    command = f"fts-rest-transfer-submit --fts-access-token {token} --src-access-token {token} --dst-access-token {token} -s {endpoint} sourcefile destfile -o"
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)

    end = datetime.now()

    # Amend test result dictionary with correct test results
    submissionResult["duration"] = str(end - start)
    submissionResult["command"] = command
    submissionResult["status"] = "PASS" if result.returncode == 0 else "FAIL"
    submissionResult["return_code"] = result.returncode
    submissionResult["output"] = result.stdout
    submissionResult["error"] = result.stderr

    # Dictionary containting information to return
    retDict = {
        "test": "fts token transfer test endpoint",
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
