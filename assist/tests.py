from django.test import TestCase
from django.test import Client
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth
from django.urls import reverse
from assist.models import PricingModel
from assist.models import AssistanceRequest
from datetime import datetime
from assist.forms import SignUpForm

#Test pricing model
class PricingTest(TestCase):
	def create_pricing(self, name="My Test Model", yearlyPrice = 12.95, calloutFee = 0, numCallouts = 0):
		return PricingModel.objects.create(name=name, yearlyPrice=yearlyPrice, calloutFee = calloutFee, numCallouts = numCallouts)

	def test_pricing_creation(self):
		bee = self.create_pricing()
		self.assertTrue(isinstance(bee, PricingModel))
		self.assertEqual(bee.__str__(), bee.name)

#Test assistance request -- kinda spicy, leaving for now..

#Index page testing
class IndexTest(TestCase):
        def test_index_status_code(self):
                response = self.client.get('/assist/')
                self.assertEquals(response.status_code, 200)

        def test_index_uses_correct_template(self):
                response = self.client.get('/assist/')
                self.assertEquals(response.status_code, 200)
                self.assertTemplateUsed(response, 'index.html')

#Login testing -- Will test POST methods after we have a login page
class LoginTest(TestCase):
        def setUp(self):
                user = User.objects.create_user(
                        username = 'buzz',
                        password = 'honey')
                user.save()

        def test_valid_login(self):
                beeClient = Client()
                response = beeClient.post(reverse('login'), {'username': 'buzz', 'password': 'honey' })
                self.assertEqual(response.status_code, 302) # Valid login will redirect!
                self.assertTrue(response.url, "/assist/dash") # Make sure it's not an invalid response though :(

        def test_invalid_login(self):
                badBeeClient = Client()
                response = badBeeClient.post(reverse('login'), {'username': 'NaughtyBee', 'password': 'aviation'})
                self.assertEqual(response.status_code, 302) # Bad login is also a redirect
                self.assertEqual(response.url, "/assist?failure=1") # Unlucky

        def test_logout(self):
                beeClient = Client()
                response = beeClient.post(reverse('login'), {'username': 'buzz', 'password': 'honey' })
                response = beeClient.get(reverse('logout'))
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url,"/assist")	# Should redirect to home page when we log out YEE HAW

#Sign-up testing
class SignUpTest(TestCase):
        def test_signup_status_code(self):
                response = self.client.get('/assist/signup')
                self.assertEqual(response.status_code, 200)

        def test_valid_user_form(self):
                beeClient = Client()
                response = beeClient.post(reverse('signup'), {'username': 'BuzzyBee', 'first_name': 'Buzzy', 'last_name': 'Bee', 'email': 'buzz@thehive.com', 'password1': 'PoxVas1221' ,'password2': 'PoxVas1221', 'address': '12 Hive Road', 'registration': 'AABBZZ', 'isServicer': 'False', 'subscription': '1'})
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, '/assist')

        def test_valid_professional_form(self):
                workerBee = Client()
                with open('test_documentation.txt') as document:
                        response = workerBee.post(reverse('signup'), {'username': 'BuzzyBee', 'first_name': 'Buzzy', 'last_name': 'Bee', 'email': 'buzz@thehive.com', 'password1': 'PoxVas1221' ,'password2': 'PoxVas1221', 'address': '12 Hive Road', 'registration': 'AABBZZ', 'isServicer': 'True', 'subscription': '1' ,'document': document})
                        self.assertEqual(response.status_code, 302)
                        self.assertEqual(response.url, '/assist')

        def test_invalid_user_form(self):
                badBee = Client()
                response = badBee.post(reverse('signup'), {}) # he posted nothiiing
                self.assertTrue(response.context['hasErrors'])
                
class lodgeRequestTest(TestCase):
        def setUp(self):
                user = User.objects.create_user(
                        username = 'buzz',
                        password = 'honey')
                user.save()
                
        def test_lodge_template(self):
                bee = Client()
                bee.post(reverse('signup'), {'username': 'BuzzyBee', 'first_name': 'Buzzy', 'last_name': 'Bee', 'email': 'buzz@thehive.com', 'password1': 'PoxVas1221' ,'password2': 'PoxVas1221', 'address': '12 Hive Road', 'registration': 'AABBZZ', 'isServicer': 'False', 'subscription': '1'})
                bee.login(username = 'BuzzyBee', password = 'PoxVas1221')
                response = bee.get('/assist/lodge', follow = True)
                self.assertTemplateUsed(response, 'lodge_view.html')

        def test_valid_lodge_form(self):
                bee = Client()
                bee.post(reverse('signup'), {'username': 'BuzzyBee', 'first_name': 'Buzzy', 'last_name': 'Bee', 'email': 'buzz@thehive.com', 'password1': 'PoxVas1221' ,'password2': 'PoxVas1221', 'address': '12 Hive Road', 'registration': 'AABBZZ', 'isServicer': 'False', 'subscription': '1'})
                bee.login(username = 'BuzzyBee', password = 'PoxVas1221')
                response = bee.post(reverse('lodge'), {'latitude': '-27.50215', 'longitude': '153.25616', 'request_details': 'There is a bear :('})
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, '/assist/dash')

        def test_invalid_lodge_form(self):
                bee = Client()
                bee.post(reverse('signup'), {'username': 'BuzzyBee', 'first_name': 'Buzzy', 'last_name': 'Bee', 'email': 'buzz@thehive.com', 'password1': 'PoxVas1221' ,'password2': 'PoxVas1221', 'address': '12 Hive Road', 'registration': 'AABBZZ', 'isServicer': 'False', 'subscription': '1'})
                bee.login(username = 'BuzzyBee', password = 'PoxVas1221')
                response = bee.post(reverse('lodge'), {'longitude': '153.25616', 'request_details': 'There is a bear :('})
                self.assertTrue(response.context['hasErrors']) # We didnt post a latitude

class ProfileTest(TestCase):
        def setUp(self):
                bee = Client()
                bee.post(reverse('signup'), {'username': 'BuzzyBee', 'first_name': 'Buzzy', 'last_name': 'Bee', 'email': 'buzz@thehive.com', 'password1': 'PoxVas1221' ,'password2': 'PoxVas1221', 'address': '12 Hive Road', 'registration': 'AABBZZ', 'isServicer': 'False', 'subscription': '1'})

        def test_profile_template(self):
                bee = Client()
                bee.login(username = 'BuzzyBee', password = 'PoxVas1221')
                response = bee.get(reverse('profile'))
                self.assertTrue(response)
                self.assertTemplateUsed(response, 'profile_view.html')

        def test_profile_update(self):
                bee = Client()
                bee.login(username = 'BuzzyBee', password = 'PoxVas1221')
                response = bee.post(reverse('profile'),{'address': '49 Hive Road', 'registration': 'BUZZZZ', 'isServicer': 'False', 'subscription': '2'})
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.url, '/assist/dash')

        def test_invalid_profile_update(self):
                bee = Client()
                bee.login(username = 'BuzzyBee', password = 'PoxVas1221')
                response = bee.post(reverse('profile'),{'address': '49 Hive Road', 'registration': 'WOWTHISISAREALLYLONGREGISTRATION', 'isServicer': 'False', 'subscription': '2'})
                self.assertTrue(response.context['hasErrors'])
