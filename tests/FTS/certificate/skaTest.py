from datetime import datetime
import shlex
import subprocess

def run_test():
    start = datetime.now()

    # Run certificate transfer to ska instance
    command = "fts-rest-transfer-submit -s https://fts3-ska.scd.rl.ac.uk sourcefile destfile -o"
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)

    end = datetime.now()

    test_result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration": str(end - start),
        "test": "fts certificate transfer ska endpoint",
        "command": command,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr,
    }

    return test_result
