from datetime import datetime
import shlex
import subprocess

def run_test():
    start = datetime.now()

    # Run certificate transfer to wlcg (prod) instance
    command = "fts-rest-transfer-submit -s https://lcgfts01.gridpp.rl.ac.uk sourcefile destfile -o"
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)

    end = datetime.now()

    test_result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration": end - start,
        "test": "fts certificate transfer wlcg endpoint",
        "command": command,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr,
    }

    return test_result
