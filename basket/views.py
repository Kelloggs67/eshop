from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from .basket import Basket
from store.models import Product
from django.http import JsonResponse
from decimal import Decimal

def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        qty = basket.basket[str(product_id)]['qty']
        basket.delete(product=product_id)
        basket_total = basket.get_total_price()
        response = JsonResponse({'Success': True, 'qty': qty, 'subtotal': basket_total})
        return response

def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)
        product_price = basket.basket[str(product_id)]['price']
        product_total_price = Decimal(product_price) * int(product_qty)
        basketqty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': basket_total, 'productprice': product_total_price})
        return response

        