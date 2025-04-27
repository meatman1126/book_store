from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
"""
AbstractUserはDjangoの標準的なユーザーモデルを拡張するための抽象基底クラス
# 既に以下のフィールドが含まれている
# username, password, first_name, last_name, email
# is_staff, is_active, is_superuser, date_joined
# 認証関連のメソッド（set_password, check_passwordなど）
"""

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True,validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='電話番号は半角数字のみで入力してください。'
            )
        ])
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # メールアドレスをユーザ名として使用する
    USERNAME_FIELD = 'email'
    # ユーザ名は必須
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
