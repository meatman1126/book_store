from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
from products.models import Product

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        RECEIVED = 'received', '注文受付'
        PAYMENT_COMPLETED = 'payment_completed', '決済完了'
        PREPARING = 'preparing', '出荷準備'
        SHIPPED = 'shipped', '出荷済'
        DELIVERED = 'delivered', '配送済'
        CANCELLED = 'cancelled', 'キャンセル'

    class PaymentMethod(models.TextChoices):
        CREDIT_CARD = 'credit_card', 'クレジットカード払い'
        CONVENIENCE = 'convenience', 'コンビニ決済'
        BANK_TRANSFER = 'bank_transfer', '銀行振込'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.RECEIVED
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CREDIT_CARD
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    shipping_address = models.TextField(default='未設定')
    shipping_name = models.CharField(max_length=100, default='未設定')
    shipping_phone = models.CharField(max_length=20, default='未設定')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-order_date']

    def __str__(self):
        return f'Order {self.id} - {self.user.email}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price_at_order = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        validators=[MinValueValidator(Decimal('0'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    def get_total_price(self):
        return self.price_at_order * self.quantity
