from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('confirm/', views.OrderConfirmView.as_view(), name='order_confirm'),
    path('complete/', views.OrderCompleteView.as_view(), name='order_complete'),
] 