from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.contrib.auth.password_validation import validate_password
import datetime

# Regex to allow only letters (including Cyrillic), dashes, apostrophes and spaces
only_letters = RegexValidator(r'^[a-zA-Zа-яА-ЯёЁ\-\' ]+$', 'Only letters are allowed.')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# Country choices
COUNTRIES = [
    ('US', 'United States'),
    ('IL', 'Israel'),
    ('UK', 'United Kingdom'),
    ('DE', 'Germany'),
    ('FR', 'France'),
    ('OTHER', 'Other'),
]

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, validators=[EmailValidator()])
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    first_name = forms.CharField(required=True, validators=[only_letters])
    last_name = forms.CharField(required=True, validators=[only_letters])
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    country = forms.ChoiceField(choices=COUNTRIES)
    agree_terms = forms.BooleanField(label="I agree to the Terms and Conditions", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password',
                  'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # 1. Password match check
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        # 2. Password complexity check using Django's built-in validators
        if password:
            try:
                validate_password(password)
            except ValidationError as e:
                self.add_error('password', e)

        # 3. Age validation (must be at least 18)
        dob = cleaned_data.get("date_of_birth")
        if dob:
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValidationError("You must be at least 18 years old to register.")

        # 4. User must agree to terms
        if not cleaned_data.get("agree_terms"):
            raise ValidationError("You must agree to the Terms and Conditions.")

        return cleaned_data
