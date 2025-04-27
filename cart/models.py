from django.db import models
from django.conf import settings
from products.models import Product
from django.utils import timezone

class Cart(models.Model):
    STATUS_CHOICES = (
        ('active', 'アクティブ'),
        ('ordered', '注文済み'),
        ('abandoned', '放棄'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'カート'
        verbose_name_plural = 'カート'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Cart ({self.status})"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def update_last_activity(self):
        self.last_activity = timezone.now()
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_added = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'カートアイテム'
        verbose_name_plural = 'カートアイテム'
        ordering = ['-created_at']
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"

    def get_total_price(self):
        return self.price_at_added * self.quantity
