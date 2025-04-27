from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

"""
admin.pyに定義することで管理者画面で管理可能になる    
"""
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 一覧表示するフィールド定義
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    # フィルタリングするフィールド定義
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    # 検索するフィールド定義
    search_fields = ('email', 'username', 'first_name', 'last_name')
    # ソートするフィールド定義
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
