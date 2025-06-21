from django import forms
from allauth.account.forms import SignupForm
from django.core.validators import RegexValidator
import datetime
from users.models import UserProfile
from orders.models import ShippingAddress
from allauth.account.models import EmailAddress


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'address', 'city', 'zip_code', 'country']


only_letters = RegexValidator(
    r'^[a-zA-Zа-яА-ЯёЁ\-\' ]+$', 'Only letters are allowed.')

COUNTRIES = [
    ('US', 'United States'),
    ('IL', 'Israel'),
    ('UK', 'United Kingdom'),
    ('DE', 'Germany'),
    ('FR', 'France'),
    ('OTHER', 'Other'),
]


class CustomSignupForm(SignupForm):
    first_name = forms.CharField(required=True, validators=[only_letters])
    last_name = forms.CharField(required=True, validators=[only_letters])
    date_of_birth = forms.DateField(
        required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    country = forms.ChoiceField(choices=COUNTRIES)
    agree_terms = forms.BooleanField(
        label="I agree to the Terms and Conditions", required=True)

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = datetime.date.today()
        age = today.year - dob.year - \
            ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise forms.ValidationError(
                "You must be at least 18 years old to register.")
        return dob

    def save(self, request):
        # создаём объект User через встроенный метод
        print("Cleaned data in save:", self.cleaned_data)
        user = super(CustomSignupForm, self).save(request)

        if user:  # добавляем проверку на None
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.save()

            # создаём профиль
            UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'country': self.cleaned_data['country'],
                    'date_of_birth': self.cleaned_data['date_of_birth'],
                }
            )

        return user


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        label="New E-mail Address",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your new email'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        # Check if the email is already in use by another user.
        if EmailAddress.objects.filter(email__iexact=email).exclude(user=self.user).exists():
            raise forms.ValidationError(
                "This e-mail address is already in use by another account.")

        # Check if the user is trying to change to their current primary email.
        primary_email = EmailAddress.objects.get_primary(self.user)
        if primary_email and email == primary_email.email:
            raise forms.ValidationError(
                "This is already your current e-mail address.")

        return email


class ChangeNameForm(forms.Form):
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name")
