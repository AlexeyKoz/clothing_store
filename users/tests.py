import datetime
from django.test import TestCase
from django.urls import reverse
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class SignupLoginTest(TestCase):

    def setUp(self):
        self.signup_url = reverse('account_signup')
        self.login_url = reverse('account_login')
        self.valid_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password1': 'TestPass123!',
            'password2': 'TestPass123!',
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': '2000-01-01',
            'country': 'IL',
            'agree_terms': True
        }

    def test_signup_success(self):
        response = self.client.post(self.signup_url, self.valid_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='testuser@example.com').exists())

    def test_signup_missing_terms(self):
        data = self.valid_data.copy()
        data['agree_terms'] = False
        response = self.client.post(self.signup_url, data)
        self.assertContains(response, "This field is required", status_code=200)

    def test_signup_with_emoji(self):
        data = self.valid_data.copy()
        data['first_name'] = '😀'
        response = self.client.post(self.signup_url, data)
        self.assertContains(response, "Only letters are allowed", status_code=200)

    def test_signup_with_invalid_symbols(self):
        data = self.valid_data.copy()
        data['last_name'] = 'User@#$%'
        response = self.client.post(self.signup_url, data)
        self.assertContains(response, "Only letters are allowed", status_code=200)

    def test_login_success(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='TestPass123!')
        response = self.client.post(self.login_url, {
            'login': 'testuser@example.com',
            'password': 'TestPass123!'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_wrong_password(self):
        User.objects.create_user(username='testuser', email='testuser@example.com', password='TestPass123!')
        response = self.client.post(self.login_url, {
            'login': 'testuser@example.com',
            'password': 'WrongPass'
        })
        self.assertContains(response, "The e-mail address and/or password you specified are not correct", status_code=200)




class SignupLoginNegativeTests(TestCase):
    def setUp(self):
        self.signup_url = reverse("account_signup")
        self.login_url = reverse("account_login")
        self.valid_data = {
            "email": "test@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
            "first_name": "Alex",
            "last_name": "Smith",
            "date_of_birth": "2000-01-01",
            "country": "IL",
            "agree_terms": True,
        }
        # Создаём пользователя заранее для проверки дубликатов
        User.objects.create_user(username="test@example.com", email="test@example.com", password="StrongPass123!")

    def test_signup_invalid_email(self):
        data = self.valid_data.copy()
        data["email"] = "🤪@@@gmail..com"
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_signup_invalid_first_name(self):
        data = self.valid_data.copy()
        data["first_name"] = "123@!"
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, "form", "first_name", "Only letters are allowed.")

    def test_signup_underage(self):
        data = self.valid_data.copy()
        data["date_of_birth"] = datetime.date.today().replace(year=datetime.date.today().year - 10).isoformat()
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, "form", "date_of_birth", "You must be at least 18 years old to register.")

    def test_signup_without_terms_agreed(self):
        data = self.valid_data.copy()
        data["agree_terms"] = False
        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, "form", "agree_terms", "This field is required.")

    def test_signup_existing_email(self):
        data = self.valid_data.copy()
        response = self.client.post(self.signup_url, data)
        self.assertContains(response, "A user is already registered with this e-mail address.")

    def test_login_wrong_email(self):
        response = self.client.post(self.login_url, {"login": "wrong@example.com", "password": "StrongPass123!"})
        self.assertContains(response, "The e-mail address and/or password you specified are not correct.")

    def test_login_wrong_password(self):
        response = self.client.post(self.login_url, {"login": "test@example.com", "password": "WrongPassword"})
        self.assertContains(response, "The e-mail address and/or password you specified are not correct.")

    def test_login_empty_fields(self):
        response = self.client.post(self.login_url, {"login": "", "password": ""})
        self.assertFormError(response, "form", "login", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")
