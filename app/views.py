from django.shortcuts import render
from .models import Job
from .filters import JobFilter


def search(request):
    job_list = Job.objects.all()
    job_filter = JobFilter(request.GET, queryset=job_list)
    # context = {'filter': job_filter}
    # return render(request, 'global/index.html', context)
    return job_filter
