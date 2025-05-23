from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserRegisterForm, UserLoginForm
from .models import UserProfile


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print("Debug, from errors: ", form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # ✅ пароль будет хэширован
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()

            # Дополнительные данные для профиля
            dob = form.cleaned_data['date_of_birth']
            country = form.cleaned_data['country']

            # Создание профиля пользователя
            UserProfile.objects.create(
                user=user,
                user_type='regular',  # можно в будущем сделать выбор
                address=f"{country}, born {dob}",  # временно сохраним туда
            )

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    return render(request, 'users/dashboard.html')
