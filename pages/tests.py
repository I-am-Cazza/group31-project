from django.test import TestCase
from app.models import CV, AppUser
import json


class UserCreationTestCase(TestCase):

    def test_user_created_correctly(self):
        data = dict()
        data['email'] = "testuser@email.com"
        data['password'] = "Apassword73"
        data['confirm_password'] = "Apassword73"
        data['first_name'] = "Test"
        data['last_name'] = "User"
        response = self.client.post('/signup/', data)
        self.assertEqual(200, response.status_code)
        newUser = AppUser.objects.get(id=1)
        self.assertNotEqual("Apassword73", password)

class JSONTestCase(TestCase):

    def test_JSON_formatted_correctly(self):
        #This function tests that data from the CV form is correctly inserted into the database in a format
        #that will be accepted by the machine learning
        s = self.client.session
        newUser = AppUser(100000, "example@email.com", "notapassword", "Applicant", False, "Firstname", "Lastname")
        newUser.save()
        s.update({
            "id": 100000,
        })
        s.save()
        data = dict()
        data['extra_field_count'] = 10
        data['extra_language_count'] = 10
        data['extra_hobby_count'] = 10
        data['extra_qual_count'] = 10
        data['extra_job_count'] = 10
        data['name'] = "testname"
        data['degree'] = "testdegree"
        data['degree_level'] = "testlevel"
        data['university'] = "testuniversity"
        for i in range(10):
            data['extra_charfield_' + str(i+1)] = "testchar"+str(i+1)
            data['extra_intfield_'+str(i+1)] = 10
            data['extra_charfield_lang_' +str(i+1)] = "testlang"+str(i+1)
            data['extra_intfield_lang_'+str(i+1)] = 10
            data['extra_charfield_hobby_'+str(i+1)] = "testhobby"+str(i+1)
            data['extra_intfield_hobby_'+str(i+1)] = 10
            data['extra_charfield_qual_'+str(i+1)] = "testqual"+str(i+1)
            data['extra_intfield_qual_'+str(i+1)] = 10
            data['extra_charfield_job_'+str(i+1)] = "testjob"+str(i+1)
            data['extra_intfield_job_'+str(i+1)] = "testpos"+str(i+1)
            data['extra_lenfield_job_'+str(i+1)] = 10

        response = self.client.post('/applicant/cv/', data)
        self.assertEqual(200, response.status_code)
        testCv = json.loads(CV.objects.get(pk=1).cvData)
        skill = testCv['Skills']
        language = testCv['Languages Known']
        hobbies = testCv['Hobbies']
        qualifications = testCv['A-Level Qualifications']
        jobs = testCv['Previous Employment']
        for i in range(10):
            self.assertEqual("testchar"+str(i+1), skill[i]["Skill"])
            self.assertEqual("testlang"+str(i+1), language[i]["Language"])
            self.assertEqual("testhobby"+str(i+1), hobbies[i]["Name"])
            self.assertEqual("testqual"+str(i+1), qualifications[i]["Qualification"])
            self.assertEqual("testjob"+str(i+1), jobs[i]["Company"])
