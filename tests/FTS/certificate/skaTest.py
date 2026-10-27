from datetime import datetime, timezone
import os
import shlex
import subprocess

from dotenv import load_dotenv

from resources.ftsTransferResults import get_job_id, get_test_result
from resources.tokenGenerator import generate_token

def run_test():
    endpoint = "https://fts3-ska.scd.rl.ac.uk:8446"
    sourceFile = "davs://xrootd-01.swesrc.chalmers.se:1094/data/src/ops_tests/service_tests/rowane2etest.txt"
    destFile = "davs://rucio.espsrc.iaa.csic.es:443/disk/ops_tests/service_tests/rowane2etest.txt"

    start = datetime.now()

    # Run certificate transfer to ska instance.
    # By using -o flag (overwrite file), we can always use the same source and destination files.
    command = f"fts-rest-transfer-submit -s {endpoint} {sourceFile} {destFile} -o"
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)

    end = datetime.now()

    submissionResult = {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "duration": str(end - start),
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr,
    }

    # Dictionary containting information to return
    retDict = {
        "test": "fts certificate transfer ska endpoint",
        "submission": submissionResult
    }

    # Generate a token to check transfer status
    load_dotenv()

    token = generate_token(
        token_endpoint="https://ska-iam.stfc.ac.uk/token",
        client_id=os.getenv("skaClientId"),
        client_secret=os.getenv("skaClientSecret")
    )

    # Check if token generation failed.
    # If so return retDict before trying to check transfer status, as without a token it will always fail.
    # Within retDict return the token generation error message.
    if not token or "OIDC" in token:
        retDict["transfer"] = {"error": f"Failed to generate a token, {token}"}
        return retDict

    # If submission and token generation succeeded,
    # retrieve the result of the transfer and return that as well.
    jobID = get_job_id(result.stdout)
    if jobID is not None:
        transferResult = get_test_result(
            endpoint=endpoint,
            jobID=jobID,
            token=token
        )

        retDict["transfer"] = transferResult

    return retDict
