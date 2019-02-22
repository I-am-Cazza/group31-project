from app.models import Job
import django_filters


class JobFilter(django_filters.FilterSet):

    class Meta:
        model = Job
        fields = {
            'job_title': ['icontains'],
            'job_desc': ['icontains'],
            'industry_type': ['icontains'],
        }


