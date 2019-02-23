from django.db import models
# from django.contrib.postgres.fields import JSONField


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=50)
    industry_type = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=50, default="group31@gmail.com")
    contact_number = models.CharField(max_length=11, default="0800970970")


class Job(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=50)
    job_desc = models.CharField(max_length=500)
    # keywords = JSONField(null=True)
    industry_type = models.CharField(max_length=50)
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

    def __str__(self):
        return self.email


class CV(models.Model):
    owner = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    # cvData = JSONField() #Uncomment on production server, not included in testing due to incompatibility with sqlite3
    cvData = models.CharField(max_length=500)


class Application(models.Model):
    userid = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    jobid = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=128)

    def __str__(self):
        return "User: " + str(self.userid) + " Job Title: " + str(self.jobid)
