from django.urls import path
from delivery_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clients-info/', views.ClientsInfoView.as_view(), name='clients-info'),
    path('create-client/', views.CreateClientView.as_view(), name='create-client'),
    path('create-order/', views.CreateOrderView.as_view(), name='create-order'),
]
