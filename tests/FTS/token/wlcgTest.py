from datetime import datetime
from dotenv import load_dotenv
import os
import shlex
import subprocess

from resources.tokenGenerator import generate_token

def run_test():
    # Prepare test_result dictionary, in case token generation fails
    test_result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration": 0,
        "test": "fts token transfer wlcg endpoint",
        "command": "",
        "status": "",
        "return_code": "",
        "output": "",
        "error": "",
    }

    load_dotenv()

    # Call the token generator with iris params
    token = generate_token(
        token_endpoint="https://iris-iam.stfc.ac.uk/token",
        client_id=os.getenv("irisClientId"),
        client_secret=os.getenv("irisClientSecret")
    )

    # Check if token generation failed. If so return test_result dictionary before test exection,
    # containing the token generation error message.
    if not token or "OIDC" in token:
        test_result["status"] = "FAIL"
        test_result["output"] = "Failed to generate a token"
        test_result["error"] = token
        return test_result

    # Token generation succeeded - attempt transfer
    start = datetime.now()

    # Run token transfer to wlcg (prod) instance
    command = f"fts-rest-transfer-submit --fts-access-token {token} --src-access-token {token} --dst-access-token {token} -s https://lcgfts01.gridpp.rl.ac.uk sourcefile destfile -o"
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)

    end = datetime.now()

    # Amend test result dictionary with correct test results
    test_result["duration"] = str(end - start)
    test_result["command"] = command
    test_result["status"] = "PASS" if result.returncode == 0 else "FAIL"
    test_result["return_code"] = result.returncode
    test_result["output"] = result.stdout
    test_result["error"] = result.stderr

    return test_result
