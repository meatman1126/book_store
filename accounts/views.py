from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import User
from .forms import CustomUserCreationForm, UserUpdateForm

# Create your views here.
# 汎用クラスベースビュー（CBV）を拡張している
# 他には関数ベースビュー（FBV）がある
# APIとして提供する場合はDjango REST framework(DRF)を使用する


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    permission_required = 'accounts.view_user'
    ordering = ['-date_joined']

    # 有効なユーザのみ表示
    def get_queryset(self):
        return User.objects.filter(is_active=True)

class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/new.html'
    success_url = reverse_lazy('login')

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/detail.html'
    context_object_name = 'user'

    def get_object(self):
        # self.requestはhttpリクエストオブジェクトにアクセスする
        # self.request.userはログインしているユーザーを表す
        return self.request.user

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/edit.html'
    success_url = reverse_lazy('accounts:detail')
    success_message = 'ユーザー情報を更新しました。'

    def get_object(self):
        return self.request.user
