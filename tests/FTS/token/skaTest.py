from datetime import datetime
from dotenv import load_dotenv
import os
import shlex
import subprocess

def run_test():
    start = datetime.now()

    load_dotenv()
    token = os.getenv("ftstoken")

    # Run token transfer to ska instance
    command = f"fts-rest-transfer-submit --fts-access-token {token} --src-access-token {token} --dst-access-token {token} -s https://fts-ska01.scd.rl.ac.uk sourcefile destfile -o"
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)

    end = datetime.now()

    test_result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration": end - start,
        "test": "fts token transfer ska endpoint",
        "command": command,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr,
    }

    return test_result
