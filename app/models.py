from django.db import models
from django.contrib.postgres.fields import JSONField


class MLModel(models.Model):
    model_name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):
        return self.model_name

    def __str__(self):
        return self.model_name

    class Meta:
        verbose_name = 'Machine Learning Model'


class MLcv (models.Model):
    model = models.ForeignKey(MLModel, on_delete=models.CASCADE)
    cv = JSONField()

    class Meta:
        verbose_name = 'Machine Learning CV'


class Organisation(models.Model):
    name = models.CharField(max_length=50)
    include_details = models.BooleanField(default=False)
    contact_email = models.CharField(max_length=50, default="group31@gmail.com")
    contact_number = models.CharField(max_length=11, default="0800970970")

    def __str__(self):
        return self.name


class Job(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    industry_type = models.ForeignKey(MLModel, default=1, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50, verbose_name="Job Title")
    job_desc = models.CharField(max_length=500, verbose_name="Job Description")
    deadline = models.DateTimeField(blank=True)

    class Meta:
        ordering = ['deadline']

    def __str__(self):
        return self.job_title


class TestQuestions(models.Model):
    question_text = models.CharField(max_length=500)
    question_answer = models.CharField(max_length=500)
    # question_type = models.CharField(max_length=500)  # MultipleChoice, LongAnswer, ShortAnswer, etc.
    question_industry = models.ForeignKey(MLModel, on_delete=models.CASCADE)  # Computing questions only asked to computing applicants, etc.

    class Meta:
        verbose_name = 'Test Question'


class AppUser(models.Model):

    userType_CHOICES = (
        ('Applicant', 'Applicant'),
        ('Employer', 'Employer'),
    )
    email = models.EmailField(max_length=64)
    password = models.CharField(max_length=500)  # Includes salt, iterations, hashing alg and hash
    userType = models.CharField(max_length=16, choices=userType_CHOICES)  # 'Applicant', etc
    cvComplete = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50,null=True)
    last_name = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.email


class CV(models.Model):
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    cvData = JSONField()


class Application(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=128)
    classification = models.CharField(max_length=128, default="Testmodel")
    answer_percent = models.FloatField(default=50.0)

    def __str__(self):
        return "User: " + str(self.user) + " Job Title: " + str(self.job)


class TestAnswers(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE) # Which application the answers belong to
    question = models.ForeignKey(TestQuestions, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Test Answer'
