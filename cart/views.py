from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem
from products.models import Product

# Create your views here.

@login_required
def cart_detail(request):
    # ユーザーのアクティブなカートを取得（なければ作成）
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        status='active'
    )
    
    # カートの最終アクティビティを更新
    cart.update_last_activity()
    
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'items': cart.items.all(),
        'total_price': cart.get_total_price(),
        'total_items': cart.get_total_items(),
    })

@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        # カートを取得または作成
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            status='active'
        )
        
        # カートアイテムを取得または作成
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={
                'quantity': quantity,
                'price_at_added': product.price
            }
        )
        
        if not created:
            # 既存のアイテムの場合は数量を更新
            cart_item.quantity += quantity
            cart_item.save()
        
        # カートの最終アクティビティを更新
        cart.update_last_activity()
        
        messages.success(request, f'{product.name}をカートに追加しました。')
        return redirect('cart:cart_detail')
    
    return redirect('products:product_detail', product_id=product_id)

@login_required
def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        
        messages.success(request, f'{product_name}をカートから削除しました。')
        return redirect('cart:cart_detail')
    
    return redirect('cart:cart_detail')

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'カートの数量を更新しました。')
        else:
            cart_item.delete()
            messages.success(request, '商品をカートから削除しました。')
        
        return redirect('cart:cart_detail')
    
    return redirect('cart:cart_detail')
