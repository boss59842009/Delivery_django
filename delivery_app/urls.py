from django.urls import path
from delivery_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients-info/', views.ClientsInfoView.as_view(), name='clients-info'),
    path('create-client/', views.CreateClientView.as_view(), name='create-client'),
    path('order/create', views.CreateOrderView.as_view(), name='create-order'),
    path('order/create-datetime/', views.CreateOrderDateTimeView.as_view(), name='create-order-datetime'),
    path('order/<int:order_number>/', views.OrderDetailView.as_view(), name='order-info'),
    path('deliveries/all', views.AllDeliveriesView.as_view(), name='all-deliveries')
]
