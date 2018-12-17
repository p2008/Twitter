from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.contrib.auth.models import Permission, User
from django.contrib.auth.views import logout_then_login
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from user_auth.forms import CreateUserForm, ResetPasswordForm, LoginForm

from twitter_app.apps import TwitterAppConfig

APP_NAME = TwitterAppConfig.name


class LoginUserView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, f'{APP_NAME}/add.html', locals())

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            next_url = request.GET.get('next')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)

                if next_url:
                    return redirect(next_url)

                return redirect(reverse('home-page'))
            else:
                form.add_error(None, 'Zły login lub hasło')
                return render(request, 'twitter_app/add.html', locals())

        form.add_error(None, 'Zły login lub hasło')
        return render(request, f'{APP_NAME}/add.html', locals())


class Password(View):

    def get(self, request, uid):
        form = ResetPasswordForm
        return render(request, f'{APP_NAME}/add.html', locals())

    def post(self, request, uid):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 == password2:
                user = get_object_or_404(User, id=uid)
                user.set_password(password1)
                user.save()
                messages.success(request, 'Hasło zostało zmienione')
            else:
                form.add_error('password1', 'Hasła nie są takie same')

        return redirect(reverse('home-page'))


class ResetPasswordView(PermissionRequiredMixin, Password):
    permission_required = 'auth.change_user'


class ChangePasswordView(LoginRequiredMixin, Password):
    login_url = f'/{APP_NAME}/login'


class CreateUserView(View):

    def get(self, request):
        form = CreateUserForm
        return render(request, f'{APP_NAME}/add.html', locals())

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            if password1 == password2:
                try:
                    User.objects.get_by_natural_key(username=email)
                except:
                    user = User.objects.create_user(username=email,
                                         first_name=first_name,
                                         last_name=last_name,
                                         email=email,
                                         password=password1)

                    # here set permissions on user
                else:
                    form.add_error('email', 'Taki użytkownik już istnieje')
            else:
                form.add_error('password', 'Hasła nie są takie same')

            return render(request, f'{APP_NAME}/login.html', locals())

        return render(request, f'{APP_NAME}/add.html', locals())


class LogoutUserView(View):

    def get(self, request):
        login_url = f'/{APP_NAME}/login/'
        return logout_then_login(request, login_url=login_url)



