from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from catalog.models import Product
from users.models import User


class UserRegistrationForm(UserCreationForm):
    """Form for user registration."""

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']


class UserProfileForm(UserChangeForm):
    """Form for updating user profile information."""

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'avatar']

    def __init__(self, *args, **kwargs):
        """Initialize the form and hide the password field."""
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()


class ResetPasswordForm(forms.Form):
    """Form for requesting a password reset via email."""

    email = forms.EmailField(label='Enter your email', max_length=254)
