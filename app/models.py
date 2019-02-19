from django.db import models
# from django.contrib.postgres.fields import JSONField

class Organisation(models.Model):
    organisation_name = models.CharField(max_length=50)
    industry_type = models.CharField(max_length=50)
    #contact_email = models.CharField(max_length=50)
    #contact_number = models.CharField(max_length=11)

class Job(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    job_title = models.CharField(max_length = 50)
    job_desc = models.CharField(max_length=500)
    # keywords = JSONField(null=True)
    industry_type = models.CharField(max_length=50)
    deadline = models.DateTimeField(blank=True)

class TestQuestions(models.Model):
    question_text = models.CharField(max_length=500)
    question_answer = models.CharField(max_length=500)
    question_type = models.CharField(max_length=500) #MultipleChoice, LongAnswer, ShortAnswer, etc.
    question_industry = models.CharField(max_length=50) #Computing questions only asked to computing applicants, etc.
