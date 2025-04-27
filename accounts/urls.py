from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('new/', views.UserCreateView.as_view(), name='new'),
    path('detail/', views.UserDetailView.as_view(), name='detail'),
    path('edit/', views.UserUpdateView.as_view(), name='edit'),
] 