from django.db import models
from django.contrib.postgres.fields import JSONField


class MLModel(models.Model):  # TODO Make Job.industry_type a foreign key of model_name?
    model_name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.model_name

    def __str__(self):
        return self.model_name


class MLcv (models.Model):
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
    cv = JSONField()


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=50)
    industry_type = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=50, default="group31@gmail.com")
    contact_number = models.CharField(max_length=11, default="0800970970")


class Job(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50 ,verbose_name="Job Title")
    job_desc = models.CharField(max_length=500,verbose_name="Job Description")
    # industry_type = models.ForeignKey(MLModel, default=1, on_delete=models.CASCADE)
    deadline = models.DateTimeField(blank=True)

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return self.job_title


class TestQuestions(models.Model):
    question_text = models.CharField(max_length=500)
    question_answer = models.CharField(max_length=500)
    question_type = models.CharField(max_length=500)  # MultipleChoice, LongAnswer, ShortAnswer, etc.
    question_industry = models.CharField(max_length=50)  # Computing questions only asked to computing applicants, etc.


class AppUser(models.Model):
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=500)  # Includes salt, iterations, hashing alg and hash
    userType = models.CharField(max_length=16)  # 'Applicant', etc
    cvComplete = models.BooleanField(default=False)
    first_name=models.CharField(max_length=50,null=True)
    last_name=models.CharField(max_length=50,null=True)
    # country=models.CharField(max_length=20,null=True)
    # city=models.CharField(max_length=20,null=True)
    # address_line_1=models.CharField(max_length=80,null=True)
    # address_line_2=models.CharField(max_length=80,null=True)
    # postal_code=models.CharField(max_length=30,null=True)
    # phone_number=models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.email


class CV(models.Model):
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    cvData = JSONField()


class Application(models.Model):
    userid = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    jobid = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=128)
    classification = models.CharField(max_length=128, default="Testmodel")
    answer_percent = models.FloatField(default=50.0)

    def __str__(self):
        return "User: " + str(self.userid) + " Job Title: " + str(self.jobid)


class TestAnswers(models.Model):
    applicationid = models.ForeignKey(Application, on_delete=models.CASCADE) # Which application the answers belong to
    questionid = models.ForeignKey(TestQuestions, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=500)
