from datetime import datetime

from django.forms import BaseModelForm
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist

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

    def form_invalid(self, form):
        client_name = self.request.POST.get('name')
        phone_number = self.request.POST.get('phone_number')
        try:
            client = models.Client.objects.get(name=client_name)
            if client:
                form = forms.CreateClientForm(instance=client)
                return render(self.request, self.template_name, {'form': form})
        except ObjectDoesNotExist:
            client = models.Client.objects.get(phone_number=phone_number)
            if client:
                form = forms.CreateClientForm(instance=client)
                return render(self.request, self.template_name, {'form': form})
    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         form.save()
    #         return redirect(self.success_url)

        # else:
        #     client_name = request.POST.get('name')
        #     phone_number = request.POST.get('phone_number')
        #     try:
        #         client = models.Client.objects.get(name=client_name)
        #         if client:
        #             form = forms.CreateClientForm(instance=client)
        #             return render(request, self.template_name, {'form': form})
        #     except ObjectDoesNotExist:
        #         client = models.Client.objects.get(phone_number=phone_number)
        #         if client:
        #             form = forms.CreateClientForm(instance=client)
        #             return render(request, self.template_name, {'form': form})


class ClientsInfoView(LoginRequiredMixin, ListView):
    model = models.Client
    context_object_name = 'clients'
    template_name = 'delivery_app/clients_info.html'


class CreateOrderView(LoginRequiredMixin, CreateView):
    template_name = 'delivery_app/create_order_form.html'
    success_url = reverse_lazy('create-order-datetime')

    def get_context_data(self, **kwargs):
        client_form = forms.CreateClientForm()
        address_form = forms.CreateDeliveryAddressForm()
        order_form = forms.CreateOrderForm()
        context = {
            'form1': client_form,
            'form2': address_form,
            'form3': order_form
        }
        return context

    def get(self, request, *args, **kwargs):
        if 'order_id' in request.session:
            del self.request.session['order_id']
        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        client_form = forms.CreateClientForm(request.POST)
        address_form = forms.CreateDeliveryAddressForm(request.POST)
        order_form = forms.CreateOrderForm(request.POST)
        if client_form.is_valid():
            client = client_form.save(commit=False)
        else:
            client_name = client_form.data['name']
            try:
                client = models.Client.objects.get(name=client_name)  # витягти клієнта з бази
            except (IntegrityError, ObjectDoesNotExist) as e:
                print(e)
                client_form.add_error('name', e)
                return render(request, self.template_name, {'form1': client_form})
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.client = client
            client.save()
        else:
            # address_form.add_error('Щось пішло не так!')
            return render(request, self.template_name, {'form2': address_form})
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.client = client
            order.manager = request.user
            order.updated_at = datetime.now()
            order.address = address
            address.save()
            order.save()
        else:
            order_form.add_error(None, 'Щось пішло не так!')
            return render(request, self.template_name, {'form3': order_form})
        request.session['order_id'] = order.id
        return redirect(reverse_lazy('create-order-datetime'))


class CreateOrderDateTimeView(LoginRequiredMixin, CreateView):
    template_name = 'delivery_app/create_order_datetime_form.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        order_id = self.request.session.get('order_id')
        order = models.OrderInfo.objects.get(id=order_id)
        order_manager = order.manager
        order_driver = self.get_driver(order)
        order.delivery_amount = self.get_delivery_price(order)
        order.save()
        self.request.session['order_driver_id'] = order_driver.id
        datetime_form = forms.CreateOrderDateTimeForm()
        context = {
            'order_manager': order_manager,
            'datetime_form': datetime_form,
            'order_driver': order_driver,
            'delivery_amount': order.delivery_amount
        }
        return context

    def get(self, request, *args, **kwargs):
        if 'order_id' in self.request.session:
            context = self.get_context_data(**kwargs)
            return render(request, self.template_name, context)
        else:
            return redirect('create-order')

    def post(self, request, *args, **kwargs):
        datetime_form = forms.CreateOrderDateTimeForm(request.POST)
        if datetime_form.is_valid():
            order_id = request.session.get('order_id')
            order_driver_id = request.session.get('order_driver_id')
            order_driver = models.Driver.objects.get(id=order_driver_id)
            order = models.OrderInfo.objects.get(id=order_id)
            order.ship_date = datetime_form.cleaned_data['ship_date']
            order.ship_time = datetime_form.cleaned_data['ship_time']
            order.driver = order_driver
            order.save()
        else:
            # raise ValidationError(datetime_form.errors)
            return render(request, self.template_name, self.context)
        return redirect('order-info', order_number=order.id)

    def get_driver(self, order):
        order_volume = order.order_volume
        order_weight = order.order_weight
        driver = models.Driver.objects.filter(vehicle_max_weight__lt=order_weight, vehicle_max_volume__lt=order_volume)
        if driver:
            return driver[0]
        else:
            driver = models.Driver.objects.get(id=1)
            return driver

    def get_delivery_price(self, order):
        price = 0
        if order.order_weight < 2000:
            price = order.distance * 30
        if 2000 <= order.order_weight < 3000:
            price = order.distance * 40
        if order.order_weight >= 3000:
            price = order.distance * 50
        if order.unload_service and order.manipulator_service:
            price *= 2.5
        elif order.unload_service:
            price *= 2
        elif order.manipulator_service:
            price *= 1.5

        return price


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'delivery_app/order_detail.html'
    model = models.OrderInfo
    context_object_name = 'order'
    pk_url_kwarg = 'order_number'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'order_id' in self.request.session:
            del self.request.session['order_id']
        if 'driver_id' in self.request.session:
            del self.request.session['driver_id']
        return context


class AllDeliveriesView(LoginRequiredMixin, ListView):
    template_name = 'delivery_app/all_deliveries.html'
    model = models.OrderInfo
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.OrderFilterForm(self.request.GET)
        return context

    def get_queryset(self):
        query_set = super().get_queryset()
        client = self.request.GET.get('client', '')
        order_number = self.request.GET.get('order', '')
        if order_number:
            query_set = query_set.filter(order_number=order_number)
        if client:
            query_set = query_set.filter(client__name=client)
        return query_set















