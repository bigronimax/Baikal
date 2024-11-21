from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from app.models import Dish
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from cart.forms import OrderForm
from django.forms import model_to_dict

def redirect_continue(request):
    continue_href = request.GET.get('continue', '/')
    return redirect(continue_href)

@login_required(login_url="login", redirect_field_name="continue")
def cartSummary(request):
    cart = Cart(request)

    cart_dishes = cart.get_dishes()
    sum_cost = cart.get_sum_cost()
    cart_quantity = cart.__len__()

    if request.method == 'GET':
        add_form = OrderForm(initial=model_to_dict(request.user))
    if request.method == 'POST':
        add_form = OrderForm(request.POST, instance=request.user, initial=model_to_dict(request.user))
        if add_form.is_valid():
            cart_dishes = cart.get_dishes()
            order = add_form.save(cart_dishes, "Hunter")
            cart.empty()
            cart_quantity = cart.__len__()
            if order:
                return redirect(reverse('hunterOrders'))
            else:
                add_form.add_error(None, 'Error with creating a new order!')

    return render(request, "hunter__cart.html", {"form": add_form, "cart_dishes": cart_dishes, "sum_cost": sum_cost, 'qty': cart_quantity})

@csrf_protect
def cartAdd(request):
    cart = Cart(request)
    
    dish_id = request.POST.get("dish_id")

    dish = get_object_or_404(Dish, id=dish_id)

    dish_qty = cart.add(dish=dish)

    cart_quantity = cart.__len__()
    sum_cost = cart.get_sum_cost()
 
    respone = JsonResponse({'qty': cart_quantity, 'dish_qty': dish_qty, "sum_cost": sum_cost})
    return respone

def cartDelete(request):
    cart = Cart(request)
    
    dish_id = request.POST.get("dish_id")

    dish = get_object_or_404(Dish, id=dish_id)

    dish_qty = cart.delete(dish=dish)

    cart_quantity = cart.__len__()
    sum_cost = cart.get_sum_cost()

    respone = JsonResponse({'qty': cart_quantity, 'dish_qty': dish_qty, "sum_cost": sum_cost})
    return respone




