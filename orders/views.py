from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import FormView, TemplateView, View
from django.urls import reverse_lazy
from django.db import transaction
from cart.models import Cart, CartItem
from .forms import OrderForm
from .models import Order, OrderItem
from products.models import Product

# Create your views here.

class OrderCreateView(LoginRequiredMixin, FormView):
    template_name = 'orders/order_create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_confirm')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(Cart, user=self.request.user, status='active')
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.warning(self.request, 'カートに商品がありません。')
            return redirect('cart:cart_detail')
        
        context.update({
            'cart': cart,
            'cart_items': cart_items,
            'total_price': cart.get_total_price(),
            'total_items': cart.get_total_items(),
        })
        return context

    def form_valid(self, form):
        # 注文情報をセッションに保存
        self.request.session['order_info'] = {
            'payment_method': form.cleaned_data['payment_method'],
            'shipping_address': form.cleaned_data['shipping_address'],
            'shipping_name': form.cleaned_data['shipping_name'],
            'shipping_phone': form.cleaned_data['shipping_phone'],
        }
        return super().form_valid(form)

class OrderConfirmView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # セッションから注文情報を取得
        order_info = request.session.get('order_info')
        if not order_info:
            messages.warning(request, '注文情報が見つかりません。')
            return redirect('orders:order_create')
        
        # カート情報を取得
        cart = get_object_or_404(Cart, user=request.user, status='active')
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.warning(request, 'カートに商品がありません。')
            return redirect('cart:cart_detail')
        
        # 支払い方法の表示名を取得
        payment_method_display = dict(Order.PaymentMethod.choices)[order_info['payment_method']]
        
        return render(request, 'orders/order_confirm.html', {
            'order_info': order_info,
            'payment_method_display': payment_method_display,
            'cart_items': cart_items,
            'total_price': cart.get_total_price(),
            'total_items': cart.get_total_items(),
        })

    def post(self, request, *args, **kwargs):
        # セッションから注文情報を取得
        order_info = request.session.get('order_info')
        if not order_info:
            messages.warning(request, '注文情報が見つかりません。')
            return redirect('orders:order_create')
        
        # カート情報を取得
        cart = get_object_or_404(Cart, user=request.user, status='active')
        cart_items = cart.items.all()
        
        if not cart_items:
            messages.warning(request, 'カートに商品がありません。')
            return redirect('cart:cart_detail')
        
        try:
            # 在庫チェック
            for cart_item in cart_items:
                if cart_item.product.stock < cart_item.quantity:
                    messages.error(request, f'{cart_item.product.name}の在庫が不足しています。')
                    return redirect('orders:order_confirm')
            
            # 注文を作成
            order = Order.objects.create(
                user=request.user,
                payment_method=order_info['payment_method'],
                shipping_address=order_info['shipping_address'],
                shipping_name=order_info['shipping_name'],
                shipping_phone=order_info['shipping_phone'],
                total_price=cart.get_total_price()
            )
            
            # 注文商品を作成し、在庫を更新
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price_at_order=cart_item.product.price
                )
                # 在庫数を更新
                cart_item.product.stock -= cart_item.quantity
                cart_item.product.save()
            
            # カートのステータスを更新
            cart.status = 'ordered'
            cart.save()
            
            # セッションから注文情報を削除
            del request.session['order_info']
            
            # 注文完了メッセージを表示
            messages.success(request, '注文が完了しました。')
            
            return redirect('orders:order_complete')
            
        except Exception as e:
            # トランザクションが自動的にロールバックされる
            messages.error(request, '注文処理中にエラーが発生しました。')
            return redirect('orders:order_confirm')

class OrderCompleteView(LoginRequiredMixin, TemplateView):
    template_name = 'orders/order_complete.html'
