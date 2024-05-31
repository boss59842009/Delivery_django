from datetime import datetime

from django.forms import BaseModelForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
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
        if client_form.is_valid():
            client = client_form.save(commit=False)
        else:
            client_name = client_form.data['name']
            client = models.Client.objects.get(name=client_name)  # витягти клієнта з бази
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.client = client
            client.save()
            address.save()
        else:
            address_form.add_error('Щось пішло не так!')
            return render(request, self.template_name, {'form1': address_form})
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.client = client
            order.manager = request.user
            order.updated_at = datetime.now()
            order.save()
        else:
            order_form.add_error(None, 'Щось пішло не так!')
            return render(request, self.template_name, {'form1': order_form})
        self.request.session['order_pk'] = order.id
        return redirect(reverse_lazy('create-order-datetime'))


class CreateOrderDateTimeView(LoginRequiredMixin, CreateView):
    template_name = 'delivery_app/create_order_datetime_form.html'
    success_url = reverse_lazy('index')
    form_class = forms.CreateOrderDateTimeForm

    def get(self, request, *args, **kwargs):
        if 'order_pk' in self.request.session:
            order_id = self.request.session.get('order_pk')
            order = models.OrderInfo.objects.get(id=order_id)
            order_manager = order.manager
            order_driver = self.get_driver(order)
            order.delivery_amount = self.get_price(order)
            order.save()
            self.request.session['order_driver_id'] = order_driver.id
            datetime_form = forms.CreateOrderDateTimeForm()
            self.context = {
                'order_manager': order_manager,
                'datetime_form': datetime_form,
                'order_driver': order_driver,
                'delivery_amount': order.delivery_amount
            }
            return render(request, self.template_name, self.context)
        else:
            return redirect('create-order')

    def post(self, request, *args, **kwargs):
        datetime_form = forms.CreateOrderDateTimeForm(request.POST)
        if datetime_form.is_valid():
            order_id = self.request.session.get('order_pk')
            order_driver_id = self.request.session.get('order_driver_id')
            order_driver = models.Driver.objects.get(id=order_driver_id)
            order = models.OrderInfo.objects.get(id=order_id)
            order.ship_date = datetime_form.cleaned_data['ship_date']
            order.ship_time = datetime_form.cleaned_data['ship_time']
            order.driver = order_driver
            order.save()
        else:
            datetime_form.add_error('Щось пішло не так!')
            return render(request, self.template_name, self.context)
        return redirect('index')

    def get_driver(self, order):
        order_volume = order.order_volume
        order_weight = order.order_weight
        driver = models.Driver.objects.filter(vehicle_max_weight__lt=order_weight, vehicle_max_volume__lt=order_volume)
        if driver:
            return driver[0]
        else:
            driver = models.Driver.objects.get(id=1)
            return driver

    def get_price(self, order):
        if order.order_weight < 1500:
            return order.order_weight
        if 1500 <= order.order_weight < 3000:
            return order.order_weight * 0.8
        if 3000 <= order.order_weight < 4500:
            return order.order_weight * 0.7
        if order.order_weight >= 4500:
            return order.order_weight * 0.6


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = models.OrderInfo
    template_name = 'delivery_app/order_detail.html'
    pk_url_kwarg = 'order_number'











