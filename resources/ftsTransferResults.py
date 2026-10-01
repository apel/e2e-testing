"""
Retrieve the results of FTS transfers.
Also has a method to retrieve just the jobID from a string.

Performs two GET requests to an FTS endpoint, using the token for token
transfers or nothing for certificate.
"""

import requests
import time


def get_job_id(output):
    for line in output.splitlines():
        if line.startswith("Job id:"):
            return line.split(":", 1)[1].strip()
    return None


def get_test_result(endpoint, jobID, token):
    # type: (str, str, str) -> dict
    """Retrieve FTS transfer results.
    Does a get on both the jobID and then its files, returning both.
    
    Args:
        endpoint (str): HTTPS URL of the token endpoint
        jobID (str): the id of the job to check
        token (str): optionally passed verification for token transfers

    Returns:
        dict: Contains result response data or an error if request(s) failed.
    """

    # Define request headers
    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Define returned dict
    totalInfo = {}

    # Attempt to get test result. wait until transfer has succeeded or failed.
    try:
        status = "submitted"
        while status == "submitted":
            # Wait 5s to give transfer time to change state
            time.sleep(5)
            resp = requests.get(
                f"{endpoint}/jobs/{jobID}",
                headers=headers,
                verify=True,
                timeout=50
            )

            if resp.json().get('job_state') != "SUBMITTED":
                status = "complete"

        resp.raise_for_status()

        jobInfo = resp.json()

        totalInfo["jobState"] = jobInfo.get('job_state')
        totalInfo["jobInfo"] = jobInfo



    except requests.exceptions.RequestException as exc:
        totalInfo["error"] = "Error retrieving job result: {}".format(exc)
        return totalInfo

    # attempt to get individual file result
    try:
        resp = requests.get(
            f"{endpoint}/jobs/{jobID}/files",
            headers=headers,
            verify=True,
            timeout=50
        )

        resp.raise_for_status()

        state = []

        for file in resp.json():
            state.append(file.get("file_state"))

        totalInfo["fileStates"] = state

        return totalInfo

    except requests.exceptions.RequestException as exc:
        totalInfo["error"] = "Error retrieving file state: {}".format(exc)
        return totalInfo
