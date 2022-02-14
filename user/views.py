from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from validate_email import validate_email
#from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.tokens import PasswordResetTokenGenerator

import threading

from django.contrib.auth import get_user_model
User = get_user_model()


class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


class RegistrationView(View):
    def get(self, request):
        return render(request, 'user/register.html')

    def post(self, request):
        context = {

            'data': request.POST,
            'has_error': False
        }

        email = request.POST.get('email')
        username = request.POST.get('email')
        full_name = request.POST.get('name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'passwords should be atleast 6 characters long')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords dont match')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Please provide a valid email')
            context['has_error'] = True

        try:
            if User.objects.get(email=email):
                messages.add_message(request, messages.ERROR, 'Email is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass

        try:
            if User.objects.get(username=username):
                messages.add_message(
                    request, messages.ERROR, 'Username is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass

        if context['has_error']:
            return render(request, 'user/register.html', context, status=400)

        user = User.objects.create_user(username=email, email=email)
        user.set_password(password)
        user.first_name = full_name
        user.last_name = full_name
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        email_subject = 'Active your Account'
        message = render_to_string('user/activate.html',
                                   {
                                       'user': user,
                                       'domain': current_site.domain,
                                       'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                       'token': generate_token.make_token(user)
                                   }
                                   )

        email_message = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )

        EmailThread(email_message).start()
        messages.add_message(request, messages.SUCCESS,
                             'Ваш аккаунт создан успешно! Пожалуйста, проверьте свой email, чтобы активировать его')

        return redirect('login')


class LoginView(View):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR,
                                 'Введите имя!')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR,
                                 'Введите пароль!')
            context['has_error'] = True
        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Неправильное имя или пароль')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'user/login.html', status=401, context=context)
        login(request, user)
        return redirect('dashboard')


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Аккаунт успешно активирован! Вы можете зайти в свой профиль')
            return redirect('login')
        return render(request, 'user/activate_failed.html', status=401)


class HomeView(View):
    def get(self, request):
        return render(request, 'main/index.html')


class LogoutView(View):
    def post(self, request):
        logout(request)
        # messages.add_message(request, messages.SUCCESS, 'Logout successfully')
        return redirect('/')


class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'user/request-reset-email.html')

    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'Пожалуйста, введите адрес email')
            return render(request, 'user/request-reset-email.html')

        user = User.objects.filter(email=email)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Сброс пароля]'
            message = render_to_string('user/reset-user-password.html',
                                       {
                                           'domain': current_site.domain,
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token': PasswordResetTokenGenerator().make_token(user[0])
                                       }
                                       )

            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email]
            )

            EmailThread(email_message).start()

        messages.success(
            request, 'Мы выслали на Ваш email инструкции, как сбросить пароль')
        return render(request, 'user/request-reset-email.html')


class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(
                    request, 'Ссылка с запросом на сброс пароля не работает, пожалуйста, пройдите процедуру заново')
                return render(request, 'user/request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            messages.success(
                request, 'Неверная ссылка')
            return render(request, 'user/request-reset-email.html')

        return render(request, 'user/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
            'has_error': False
        }

        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Пароль должен быть не короче 6 символов!')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'пароль не совпадает')
            context['has_error'] = True

        if context['has_error'] == True:
            return render(request, 'user/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))

            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(
                request, 'Новый пароль успешно установлен, зайдите в систему используя новый пароль')

            return redirect('login')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Что-то пошло не так')
            return render(request, 'user/set-new-password.html', context)

        return render(request, 'user/set-new-password.html', context)
