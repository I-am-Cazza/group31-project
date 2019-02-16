from .models.py import Job

def keyword_filter(keyword):
    results = Job.objects.filter(job_desc__contains(keyword))
    return results
