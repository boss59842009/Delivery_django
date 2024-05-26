from datetime import datetime

from django.forms import BaseModelForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from delivery_app import models
from delivery_app import forms


def index(request):
    context = {
        'render_string': 'Hello, world!'
    }
    return render(request, template_name='delivery_app/index.html', context=context)


class CreateClientView(LoginRequiredMixin, CreateView):
    title = "Створення клієнта"
    model = models.Client
    template_name = 'delivery_app/client_form.html'
    form_class = forms.CreateClientForm
    success_url = reverse_lazy('clients-info')


class ClientsInfoView(LoginRequiredMixin, ListView):
    model = models.Client
    context_object_name = 'clients'
    template_name = 'delivery_app/clients_info.html'


class CreateOrderView(LoginRequiredMixin, CreateView):
    template_name = 'delivery_app/create_order.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        client_form = forms.CreateClientForm()
        address_form = forms.CreateDeliveryAddressForm()
        order_form = forms.CreateOrderInfoForm()
        context = {
            'form1': client_form,
            'form2': address_form,
            'form3': order_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        client_form = forms.CreateClientForm(request.POST)
        address_form = forms.CreateDeliveryAddressForm(request.POST)
        order_form = forms.CreateOrderInfoForm(request.POST)
        try:
            client_form.is_valid()
            client = client_form.save()
        except (IntegrityError, ValueError):
            client_name = client_form.data['name']
            client = models.Client.objects.get(name=client_name)  # витягти клієнта з бази
        if address_form.is_valid():
            address_form.is_valid()
            address = address_form.save(commit=False)
            address.client = client
            address.save()
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.client = client
            order.manager = request.user
            order.updated_at = datetime.now()
            order.save()
        else:
            print('is not valid')
            raise ValidationError(order_form.errors)
        return redirect('index')


        # else:
        #     return redirect('clients-info')

    # def save_forms(self, *forms):

        # try:
        #     client = forms[0].save()
        # except IntegrityError:
        #     client_name = forms[0].cleaned_data['name']
        #     client = models.Client.objects.get(name=client_name)  # витягти клієнта з бази
        # if forms[1].is_valid():
        #     address = forms[1].save(commit=False)
        #     address.client = client
        #     address.save()
        #     if forms[2].is_valid():
        #         order = forms[2].save(commit=False)
        #         order.client = client  # звʼязати з клієнтом
        #         order.manager = request.user
        #         order.save()














