from datetime import datetime

from django.forms import BaseModelForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, ListView, View
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
    template_name = 'delivery_app/create_order_form.html'
    success_url = reverse_lazy('create-order-datetime')

    def get(self, request, *args, **kwargs):
        client_form = forms.CreateClientForm()
        address_form = forms.CreateDeliveryAddressForm()
        order_form = forms.CreateOrderForm()
        context = {
            'form1': client_form,
            'form2': address_form,
            'form3': order_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        client_form = forms.CreateClientForm(request.POST)
        address_form = forms.CreateDeliveryAddressForm(request.POST)
        order_form = forms.CreateOrderForm(request.POST)
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
        self.request.session['order_pk'] = order.id
        return redirect(reverse_lazy('create-order-datetime'))


class CreateOrderDateTimeView(LoginRequiredMixin, CreateView):
    template_name = 'delivery_app/create_order_datetime.html'
    success_url = reverse_lazy('index')
    form_class = forms.CreateOrderDateTimeForm

    def get(self, request, *args, **kwargs):
        if 'order_pk' in self.request.session:
            order_id = self.request.session.get('order_pk')
            order = models.OrderInfo.objects.get(id=order_id)
            order_manager = order.manager
            order_driver = self.get_driver(order)
            self.request.session['order_driver_id'] = order_driver.id
            datetime_form = forms.CreateOrderDateTimeForm()
            context = {
                'order_manager': order_manager,
                'datetime_form': datetime_form,
                'order_driver': order_driver
            }
            return render(request, self.template_name, context)
        else:
            return redirect('create-order')

    def post(self, request, *args, **kwargs):
        datetime_form = forms.CreateOrderDateTimeForm(request.POST)
        try:
            datetime_form.is_valid()
            order_id = self.request.session.get('order_pk')
            order_driver_id = self.request.session.get('order_driver_id')
            order_driver = models.Driver.objects.get(id=order_driver_id)
            order = models.OrderInfo.objects.get(id=order_id)
            order.ship_date = datetime_form.cleaned_data['ship_date']
            order.ship_time = datetime_form.cleaned_data['ship_time']
            order.driver = order_driver
            order.save()
        except:
            raise ValidationError(datetime_form.errors)
        return redirect('index')

    def get_driver(self, order):
        order_volume = order.order_volume
        order_weight = order.order_weight
        driver = models.Driver.objects.filter(vehicle_max_weight__lt=order_weight, vehicle_max_volume__lt=order_volume)
        return driver[0]













