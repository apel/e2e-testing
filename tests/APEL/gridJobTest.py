from datetime import datetime
import shlex
import subprocess

def run_test():
    start = datetime.now()

    # Run grid job. Assume job description file already exists
    command = "arcsub -C arc-ce-test01.gridpp.rl.ac.uk -T arcrest testjobdesc.xrsl"
    result = subprocess.run(shlex.split(command), capture_output=True, text=True)

    end = datetime.now()

    test_result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duration": end - start,
        "test": "apel grid job",
        "command": command,
        "status": "PASS" if result.returncode == 0 else "FAIL",
        "return_code": result.returncode,
        "output": result.stdout,
        "error": result.stderr,
    }

    # If test passed, retrieve jobid and add to test_result dictionary
    if result.returncode == 0:
        jobid = result.stdout.split("jobid:")[1].strip()
        test_result["jobid"] = jobid

    return test_result
