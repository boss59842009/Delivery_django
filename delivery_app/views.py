from django.forms import BaseModelForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from delivery_app import models
from delivery_app import forms


def index(request):
    context = {
        'render_string': 'Hello, world!'
    }
    return render(request, template_name='delivery_app/index.html', context=context)


class CreateClientView(CreateView):
    title = "Створення клієнта"
    model = models.Client
    template_name = 'delivery_app/client_form.html'
    form_class = forms.ClientForm
    success_url = reverse_lazy('clients-info')


class ClientsInfoView(ListView):
    model = models.Client
    context_object_name = 'clients'
    template_name = 'delivery_app/clients_info.html'

# def clients_info(request):
#     clients = models.Client.objects.all()
#     context = {
#         'clients': clients
#     }
#     return render(request, template_name='delivery_app/clients_info.html', context=context)


class CustomLoginView(LoginView):
    template_name = 'delivery_app/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'login'


class RegisterView(CreateView):
    template_name = 'delivery_app/register.html'
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy('login'))













