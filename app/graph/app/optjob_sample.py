from modules.optjob.client import get_job, get_job_result_as_str, optjob_client

job_id = "52cd725b-66b5-4b2e-98b2-3da36fa317c9"
job = get_job(job_id)
print(job.data)

result = get_job_result_as_str(job_id)
print(result)
