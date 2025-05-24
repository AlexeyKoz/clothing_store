from django.test import TestCase
from django.urls import reverse

class UserRegisterValidationTests(TestCase):

    def base_valid_data(self):
        return {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securePass123',
            'confirm_password': 'securePass123',
            'first_name': 'Alex',
            'last_name': 'Kozlov',
            'date_of_birth': '2000-01-01',
            'country': 'US',
            'agree_terms': True
        }

    def test_first_name_required_and_clean(self):
        data = self.base_valid_data()
        data['first_name'] = ''
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("first_name", response.context['form'].errors)

        data['first_name'] = '!!!'  # недопустимые символы
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("first_name", response.context['form'].errors)

    def test_last_name_required_and_clean(self):
        data = self.base_valid_data()
        data['last_name'] = ''
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("last_name", response.context['form'].errors)

        data['last_name'] = '😂'
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("last_name", response.context['form'].errors)

    def test_valid_date_of_birth_and_age(self):
        data = self.base_valid_data()
        data['date_of_birth'] = '2020-01-01'
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("__all__", response.context['form'].errors)
        self.assertIn("at least 18 years", str(response.context['form'].errors['__all__']))


    def test_invalid_email_format(self):
        data = self.base_valid_data()
        data['email'] = 'not-an-email'
        response = self.client.post(reverse('register'), data)
        self.assertIn("email", response.context['form'].errors)
