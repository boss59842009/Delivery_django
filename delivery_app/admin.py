from django.contrib import admin

from delivery_app.models import Client, DeliveryAddress, Driver, OrderInfo


admin.site.register(Client)
admin.site.register(DeliveryAddress)
admin.site.register(Driver)
admin.site.register(OrderInfo)
