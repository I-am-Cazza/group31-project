from django.test import TestCase
from app.models import CV, AppUser, TestQuestions, TestAnswers, MLModel, Organisation, Job, Application
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
        self.assertNotEqual("Apassword73", newUser.password)

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
        #data['degree_level'] = "1st"
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
        testCv = json.loads(CV.objects.get(pk=0).cvData)
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

class QuestionTestCase(TestCase):
    def test_questions_evaluated_correctly(self):
        s = self.client.session
        newUser = AppUser(100000, "example@email.com", "notapassword", "Applicant", False, "Firstname", "Lastname")
        newUser.save()
        s.update({
            "id": 100000,
        })
        s.save()
        data = dict()
        testML = MLModel(1, "TestModel")
        testML.save()
        testOrganisation = Organisation(1, "TestOrg", True, "testemail@email.com", "01234567890")
        testOrganisation.save()
        testJob = Job(1, 1, 1, "TestJob", "TestDesc", "2019-03-15")
        testJob.save()

        testCV = CV(1, 1, '{"Name": "Bill", "Degree Qualification": "Computer Science BSc", "Degree Level": "1st", "University Attended": "University of Warwick", "Skills": [{"Skill": "Server setup", "Expertise": 10}, {"Skill": "Database Management", "Expertise": 10}], "Languages Known": [{"Language": "Python", "Expertise": 10}, {"Language": "Java", "Expertise": 10}, {"Language": "C#", "Expertise": 10}], "Hobbies": [{"Name": "Gaming", "Interest": 10}], "A-Level Qualifications": [{"Subject": "Computer Science", "Grade": "A"}, {"Subject": "Chemistry", "Grade": "A"}], "Previous Employment": [{"Company": "Microsoft", "Position": "CEO", "Length of Employment": 120}]}')
        test_question_one = TestQuestions(1, "What is 5 + 3?", "8", 1)
        test_question_one.save()
        test_question_two = TestQuestions(2, "What is 9 + 5?", "14", 1)
        test_question_two.save()
        test_question_three = TestQuestions(3, "What is 12 + 4?", "16", 1)
        test_question_three.save()
        test_question_four = TestQuestions(4, "What is 15 + 16?", "31", 1)
        test_question_four.save()
        data['extra_questionfield_0'] = "8"
        data['extra_questionfield_1'] = "14"
        data['extra_questionfield_2'] = "16"
        data['extra_questionfield_3'] = "73"
        response = self.client.post('/applicant/test/1/', data)
        self.assertEqual(200, response.status_code)
        newApplication = Application.objects.get(id=1)
        self.assertEqual(75.0, newApplication.answer_percent)
