from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['shipping_name'].initial = user.get_full_name() or user.username
            self.fields['shipping_phone'].initial = user.phone_number
            self.fields['shipping_address'].initial = user.address

    class Meta:
        model = Order
        fields = ['payment_method', 'shipping_address', 'shipping_name', 'shipping_phone']
        widgets = {
            'payment_method': forms.RadioSelect(choices=Order.PaymentMethod.choices, attrs={
                'class': 'space-y-2'
            }),
            'shipping_address': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'shipping_name': forms.TextInput(attrs={
                'placeholder': '例：山田 太郎',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
            'shipping_phone': forms.TextInput(attrs={
                'placeholder': '例：090-1234-5678',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
            }),
        }
        labels = {
            'payment_method': '支払い方法',
            'shipping_address': '配送先住所',
            'shipping_name': 'お名前',
            'shipping_phone': '電話番号',
        } 