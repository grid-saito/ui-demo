import os
import tempfile
import zipfile

from config import (OPTJOB_HOST, OPTJOB_JOB_QUEUE_ID, OPTJOB_PROJECT_ID,
                    OPTJOB_TOKEN)
from optjob.client import OptJobClient

# Project id and job queue id are required to submit a job.
optjob_client = OptJobClient(token=OPTJOB_TOKEN, host=OPTJOB_HOST, verbose=True)


def get_job(job_id: str):
    return optjob_client.get_job(project_id=OPTJOB_PROJECT_ID, job_id=job_id)

def get_job_result_as_str(job_id: str) -> str:
    response = optjob_client.get_job_sol(project_id=OPTJOB_PROJECT_ID, job_id=job_id)
    extract_path = "./"
    with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as tmp:
        zip_path = tmp.name
        with open(zip_path, "wb") as f:
            f.write(response.file.read())

        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(extract_path)

    with open(os.path.join(extract_path, "solution.sol"), "r") as f:
        result = f.read()

    return result
