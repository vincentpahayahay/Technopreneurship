from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from store.models import Category
from django.contrib import messages


def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    categ = Category.objects.all()
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {'cart_products':cart_products, 'categ': categ, 'quantities':quantities, 'totals':totals})

def cart_add(request):
    cart = Cart(request)   
    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()
        #response = JsonResponse({'Product Name': product.name})
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added To Cart..."))
        return response

'''
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty': product_qty})
        return response
'''
def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))  # Convert to string to match cart keys
        product_qty = int(request.POST.get('product_qty'))

        if product_id in cart.cart:  # Check if product exists in the cart
            cart.update(product=product_id, quantity=product_qty)
            response = JsonResponse({'qty': product_qty})
            messages.success(request, ("Your Cart Has Been Updated..."))
        else:
            response = JsonResponse({'error': 'Product not in cart'}, status=400)

        return response
    
def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = str(request.POST.get('product_id'))  # Convert to string for consistency

        if product_id in cart.cart:  # Ensure product exists before removing
            cart.delete(product=product_id)
            response = JsonResponse({'success': True})
            messages.success(request, ("Product Has Been Deleted..."))
        else:
            response = JsonResponse({'error': 'Product not found in cart'}, status=400)

        return response
