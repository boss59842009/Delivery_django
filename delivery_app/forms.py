from django import forms
from delivery_app.models import Client, DeliveryAddress, OrderInfo


class CreateClientForm(forms.ModelForm):
    title = 'Дані про клієнта'

    class Meta:
        model = Client
        fields = ['name', 'phone_number']
        labels = {
            'name': "Імʼя",
            'phone_number': 'Номер телефону'
        }


class CreateDeliveryAddressForm(forms.ModelForm):
    title = 'Адреса клієнта'

    class Meta:
        model = DeliveryAddress
        fields = ['city', 'street', 'house', 'apartment']
        labels = {
            'city': "Населений пункт",
            'street': 'Вулиця',
            'house': 'Будинок',
            'apartment': 'Квартира',
        }


class CreateOrderForm(forms.ModelForm):
    title = 'Дані доставки'

    class Meta:
        model = OrderInfo
        fields = [
            'order_number',
            'order_weight',
            'order_volume',
            'order_amount',
            'order_adress',
            'unload_service',
            'manipulator_service',
            'additional_info'
        ]
        labels = {
            'order_number': "Номер замовлення",
            'order_weight': 'Вага замовлення',
            'order_volume': "Обʼєм замовлення",
            'order_amount': 'Сума замовлення',
            'order_adress': "Склад відвантаження",
            'unload_service': 'Розвантаження замовлення',
            'manipulator_service': 'Послуги маніпулятора',
            'additional_info': 'Додаткова інформація',
        }


class CreateOrderDateTimeForm(forms.ModelForm):
    title = 'Дата та час доставки'

    class Meta:
        model = OrderInfo
        fields = ['ship_date', 'ship_time']
        labels = {
            'ship_date': 'Дата доставки',
            'ship_time': 'Час доставки',
            # 'driver': 'Підбір транспорту'
        }























