from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
import datetime

class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

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
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    country = forms.ChoiceField(choices=COUNTRIES)
    agree_terms = forms.BooleanField(label="I agree to the Terms and Conditions", required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password',
                  'first_name', 'last_name']  # 👈 только поля модели

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()

        # Confirm password match
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")

        # Age check
        dob = cleaned_data.get("date_of_birth")
        if dob:
            today = datetime.date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            if age < 18:
                raise ValidationError("You must be at least 18 years old to register.")

        # Terms agreement check
        if not cleaned_data.get("agree_terms"):
            raise ValidationError("You must agree to the Terms and Conditions.")

        return cleaned_data
