from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from .models import User

# ユーザー登録フォーム
# Django標準のUserCreationFormを継承して、emailフィールドを追加
# 標準ではusernameフィールドが必須でだがemailフィールドをログインIDとして使用する
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        error_messages={
            'required': _('メールアドレスを入力してください。'),
            'invalid': _('有効なメールアドレスを入力してください。'),
        }
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
        error_messages = {
            'password2': {
                'password_mismatch': _('パスワードが一致しません。'),
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].error_messages = {
            'required': _('パスワードを入力してください。'),
            'min_length': _('パスワードは8文字以上で入力してください。'),
            'password_too_common': _('このパスワードは一般的すぎます。'),
            'password_entirely_numeric': _('パスワードを数字のみにすることはできません。'),
        }
        self.fields['password2'].error_messages = {
            'required': _('パスワード（確認）を入力してください。'),
        }

    # saveメソッドをオーバーライドして、emailをusernameとして使用
    def save(self, commit=True):
        # ユーザーを作成しないで、ユーザーのフィールドを設定(commit=Falseは定番の手法)
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['email']  # emailをusernameとして使用
        
        if commit:
            user.save()
            # 新規ユーザーを一般ユーザーグループに追加
            try:
                general_user_group = Group.objects.get(name='一般ユーザ')
                user.groups.add(general_user_group)
            except Group.DoesNotExist:
                # グループが存在しない場合は作成
                general_user_group = Group.objects.create(name='一般ユーザ')
                user.groups.add(general_user_group)
        
        return user 

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone_number', 'address')
        labels = {
            'first_name': _('名'),
            'last_name': _('姓'),
            'phone_number': _('電話番号'),
            'address': _('住所'),
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-input border border-gray-300 rounded px-3 py-2 w-full'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input border border-gray-300 rounded px-3 py-2 w-full'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input border border-gray-300 rounded px-3 py-2 w-full'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-textarea border border-gray-300 rounded px-3 py-2 w-full'
            }),
        } 