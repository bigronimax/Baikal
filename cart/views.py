from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from app.models import Dish, Restaurant
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
def cartSummary(request, restaurant_name):
    restaurant = Restaurant.objects.get_by_name(restaurant_name)[0]
    cart = Cart(request)

    cart_dishes = cart.get_dishes(restaurant_name=restaurant_name)
    sum_cost = cart.get_sum_cost(restaurant_name=restaurant_name)
    cart_quantity = cart.__len__(restaurant_name=restaurant_name)

    if request.method == 'GET':
        add_form = OrderForm(initial=model_to_dict(request.user))
    if request.method == 'POST':
        add_form = OrderForm(request.POST, instance=request.user, initial=model_to_dict(request.user))
        if add_form.is_valid():
            cart_dishes = cart.get_dishes(restaurant_name=restaurant_name)
            order = add_form.save(restaurant_name=restaurant_name)
            for dish in cart_dishes:
                dish.order = order
                dish.save()
            cart.empty(restaurant_name=restaurant_name)
            cart_quantity = cart.__len__(restaurant_name=restaurant_name)
            if order:
                return redirect(reverse('restaurantOrders', args=(restaurant_name, )))
            else:
                add_form.add_error(None, 'Error with creating a new order!')

    return render(request, "restaurant__cart.html", {"form": add_form, "cart_dishes": cart_dishes, "sum_cost": sum_cost, 'qty': cart_quantity, "restaurant": restaurant})

@csrf_protect
def cartAdd(request, restaurant_name):
    cart = Cart(request)
    
    dish_id = request.POST.get("dish_id")

    dish = get_object_or_404(Dish, id=dish_id)

    dish_qty = cart.add(dish=dish, restaurant_name=restaurant_name)

    cart_quantity = cart.__len__(restaurant_name=restaurant_name)
    sum_cost = cart.get_sum_cost(restaurant_name=restaurant_name)
 
    respone = JsonResponse({'qty': cart_quantity, 'dish_qty': dish_qty, "sum_cost": sum_cost})
    return respone

def cartDelete(request, restaurant_name):
    cart = Cart(request)
    
    dish_id = request.POST.get("dish_id")

    dish = get_object_or_404(Dish, id=dish_id)

    dish_qty = cart.delete(dish=dish, restaurant_name=restaurant_name)

    cart_quantity = cart.__len__(restaurant_name=restaurant_name)
    sum_cost = cart.get_sum_cost(restaurant_name=restaurant_name)

    respone = JsonResponse({'qty': cart_quantity, 'dish_qty': dish_qty, "sum_cost": sum_cost})
    return respone




