from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user = {
            'email':'test@gmail.com',
            'username':'username',
            'password':'password',
            'password2':'password',
            'name':'fullname'
        }
        self.user_short_password = {
            'email':'test@gmail.com',
            'username':'username',
            'password':'pass',
            'password2':'pass',
            'name':'fullname'
        }
        self.user_unmatch_password = {
            'email':'test@gmail.com',
            'username':'username',
            'password':'pass1234',
            'password2':'pass5678',
            'name':'fullname'
        }
        self.user_invalid_email = {
            'email':'testagmail.com',
            'username':'username',
            'password':'pass1234',
            'password2':'pass5678',
            'name':'fullname'
        }
        self.user_blank_username = {
            'email':'test@gmail.com',
            'username':'',
            'password':'password',
            'password2':'password',
            'name':'fullname'
        }
        self.user_blank_fullname = {
            'email':'test@gmail.com',
            'username':'username',
            'password':'password',
            'password2':'password',
            'name':''
        }

        return super().setUp()

class RegisterTest(BaseTest):
    def test_can_view_page_correctly(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'auth/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.register_url,self.user,format="text/html")
        self.assertEqual(response.status_code,302)

    def test_can_register_user_with_short_password(self):
        response = self.client.post(self.register_url,self.user_short_password,format="text/html")
        self.assertEqual(response.status_code,400)

    def test_can_register_user_unmatch_password(self):
        response = self.client.post(self.register_url,self.user_unmatch_password,format="text/html")
        self.assertEqual(response.status_code,400)

    def test_can_register_user_invalid_email(self):
        response = self.client.post(self.register_url,self.user_invalid_email,format="text/html")
        self.assertEqual(response.status_code,400)

    def test_can_register_user_taken_email(self):
        self.client.post(self.register_url,self.user,format="text/html")
        response = self.client.post(self.register_url,self.user,format="text/html")
        self.assertEqual(response.status_code,400)

    def test_can_register_user_blank_username(self):
        response = self.client.post(self.register_url,self.user_blank_username,format="text/html")
        self.assertEqual(response.status_code,400)

    def test_can_register_user_blank_fullname(self):
        response = self.client.post(self.register_url,self.user_blank_fullname,format="text/html")
        self.assertEqual(response.status_code,400)


class LoginTest(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'auth/login.html')

    def test_login_success(self):
        self.client.post(self.register_url,self.user,format="text/html")
        user = User.objects.filter(email=self.user['email']).first()
        user.is_active = True
        user.save()
        response = self.client.post(self.login_url,self.user,format="text/html")
        self.assertEqual(response.status_code,302)

    def test_cant_login_with_unverified_email(self):
        self.client.post(self.register_url,self.user,format="text/html")
        response = self.client.post(self.login_url,self.user,format="text/html")
        self.assertEqual(response.status_code,401)

    def test_cant_login_with_blank_username(self):
        response = self.client.post(self.login_url,{'username':'','password':'testpassword'},format="text/html")
        self.assertEqual(response.status_code,401)
    
    def test_cant_login_with_blank_password(self):
        response = self.client.post(self.login_url,{'username':'someusername','password':''},format="text/html")
        self.assertEqual(response.status_code,401)