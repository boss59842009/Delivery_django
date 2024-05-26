from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, ListView
from django.contrib.auth import login
from django.urls import reverse_lazy

from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'delivery_app/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'


class RegisterView(CreateView):
    template_name = 'delivery_app/register.html'
    form_class = CustomUserCreationForm
    model = CustomUser

    def form_valid(self, form):
        user = form.save()
        print(user)
        login(self.request, user)
        return redirect(reverse_lazy('login'))
