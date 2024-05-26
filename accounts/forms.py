from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput, EmailInput

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email') + UserCreationForm.Meta.fields
        labels = {
            'first_name': 'Імʼя',
            'last_name': 'Прізвище',
            'email': 'Email',
            'phone_number': 'Номер телефону',
            'username': 'Username',
            'password1': 'Пароль',
            'password2': 'Підтвердити пароль',
        }
