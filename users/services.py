import string

from random import choice

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from djangoProject import settings
from users.models import User


def generate_password(length=8):
    pre_pass = string.ascii_letters + string.digits
    return ''.join(choice(pre_pass) for _ in range(length))


def make_new_password(email):
    try:
        user = User.objects.get(email=email)
        new_pass = generate_password()
        user.password = make_password(new_pass)
        user.save()

        send_mail(
            subject=f"Востановление пароля",
            message=f"Вот ваш новый пароль: {new_pass}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )

        return True, 'Новый пароль был отправлен на ваш email.'
    except User.DoesNotExist:
        return False, "Пользователя с такием email не существует"
