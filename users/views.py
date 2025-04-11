from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from djangoProject import settings
from users.forms import UserRegistrationForm, UserProfileForm, ResetPasswordForm
from users.models import User
from users.services import make_new_password


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        email = form.cleaned_data.get("email")

        send_mail(
            subject="Подтверждение регистрации",
            message=f"Здравствуйте! Вы успешно зарегистрировались!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        return response


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class ResetPasswordView(View):
    def get(self, request):
        form = ResetPasswordForm()
        return render(request, template_name='users/password_reset.html', context={'form': form})

    def post(self, request):
        form = ResetPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            flag, message = make_new_password(email)
            if flag:
                messages.success(request, message)
                return redirect('users:login')

            messages.error(request, message)

        return render(request, 'users/password_reset.html', {'form': form})
