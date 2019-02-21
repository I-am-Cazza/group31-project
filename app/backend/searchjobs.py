from app.models import Job


def keyword_filter(keyword):
    results = Job.objects.get(job_desc__icontains=keyword)
    return results


def title_search(title):
    results = Job.objects.filter(job_title__icontains=title)
    return results


def industry_filter(keyword):
    results = Job.objects.filter(industry_type__icontains=keyword)
    return results
