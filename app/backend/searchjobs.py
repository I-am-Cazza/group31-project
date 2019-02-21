from app.models import Job


def keyword_filter(keyword):
    results = Job.objects.filter(job_desc__contains(keyword))
    return results


def title_search(title):
    results = Job.objects.filter(job_title__contains(title))
    return results


def industry_filter(keyword):
    results = Job.object.filter(industry_type__contains(keyword))
    return results
