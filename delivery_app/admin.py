from django.contrib import admin

from delivery_app.models import Client, DeliveryAddress, Driver, Manager, OrderInfo

admin.site.register(Client)
admin.site.register(DeliveryAddress)
admin.site.register(Driver)
admin.site.register(Manager)
admin.site.register(OrderInfo)
