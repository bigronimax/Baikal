from django.shortcuts import render, redirect
from . import models
from django.contrib import auth
import app.forms
from math import ceil
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from .models import Reservation
from django.shortcuts import Http404
from django.core.paginator import Paginator
from calendar import Calendar, monthrange
import datetime

c = Calendar()

def calculate_profit(restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    month_size = monthrange(datetime.date.today().year, datetime.date.today().month)[1]
    for d in [x for x in c.itermonthdates(datetime.date.today().year, datetime.date.today().month) if x.month == datetime.date.today().month]:
        revenue = models.Revenue.objects.get(date=d)
        revenue.guests = models.Order.objects.get_sum_guests_by_restaurant_date(restaurant_name, d)
        revenue.income = models.Order.objects.get_sum_cost_by_restaurant_date(restaurant_name, d)
        revenue.consumption = models.Supply.objects.get_sum_cost_by_restaurant(restaurant_name) + (models.Worker.objects.get_sum_cost_by_restaurant(restaurant_name) // month_size)
        revenue.profit = revenue.income - revenue.consumption
        revenue.restaurant = restaurant
        revenue.save()
    return models.Revenue.objects.get_by_current_month_and_restaurant(restaurant_name)

def paginate(request, objects, per_page=3):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_items = paginator.page(page_number)
    num_pages = paginator.num_pages
    return {'items': page_items, 'obj': page_obj, 'num': num_pages}

def main(request):
    restaurants = models.Restaurant.objects.all
    return render(request, "main.html", {"restaurants": restaurants})

def restaurantIndex(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    return render(request, "restaurant__index.html", {"restaurant": restaurant})

def restaurantReservation(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    if request.method == 'POST':
        reservation_form = app.forms.ReservationAddForm(request.POST)
        if reservation_form.is_valid():
            reservation_form.save(restaurant_name=restaurant_name)
            return redirect(reverse('restaurantIndex', args=(restaurant_name, )))
    else:
        reservation_form = app.forms.ReservationAddForm()
        
    return render(request, "restaurant__reservation.html", {'form': reservation_form, "restaurant": restaurant})

def restaurantMenu(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    return render(request, "restaurant__menu.html", context={"restaurant": restaurant})

def restaurantReviews(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    reviews = paginate(request, models.Review.objects.get_new_by_restaurant(restaurant_name))['items']
    page_obj = paginate(request, models.Review.objects.get_new_by_restaurant(restaurant_name))['obj']
    num_pages = paginate(request, models.Review.objects.get_new_by_restaurant(restaurant_name))['num']
    return render(request, "restaurant__reviews.html", context={"reviews": reviews, "page_obj": page_obj, "num_pages": num_pages, "restaurant": restaurant})

@login_required(login_url="login", redirect_field_name="continue")
def restaurantOrders(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    orders = paginate(request, models.Order.objects.get_all_by_user_and_restaurant(request.user, restaurant_name))['items']
    page_obj = paginate(request, models.Order.objects.get_all_by_user_and_restaurant(request.user, restaurant_name))['obj']
    num_pages = paginate(request, models.Order.objects.get_all_by_user_and_restaurant(request.user, restaurant_name))['num']
    return render(request, "restaurant__orders.html", context={"orders": orders, "page_obj": page_obj, "num_pages": num_pages, "restaurant": restaurant})

def restaurantOrderItem(request, restaurant_name, order_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    try:
        order = models.Order.objects.get(id=order_id)
    except models.Order.DoesNotExist:
        raise Http404('Order does not exist')
    sum_cost = models.Order.objects.get_sum_cost_by_id(order_id)
    return render(request, "restaurant__orderItem.html", {"order": order, "sum_cost": sum_cost, "restaurant": restaurant})

def restaurantAdmin(request):
    restaurants = models.Restaurant.objects.all()
    return render(request, "restaurant__admin.html", {"restaurants": restaurants})

def restaurantAdminEdit(request, restaurant_name):
    try:
        restaurant = models.Restaurant.objects.get(name=restaurant_name)
    except models.Restaurant.DoesNotExist:
        raise Http404('Restaurant does not exist')

    if request.method == 'GET':
        edit_form = app.forms.RestaurantEditForm(initial=model_to_dict(models.Restaurant.objects.get(name=restaurant_name)))
    if request.method == 'POST':
        edit_form = app.forms.RestaurantEditForm(request.POST, request.FILES, instance=models.Restaurant.objects.get(name=restaurant_name), initial=model_to_dict(models.Restaurant.objects.get(name=restaurant_name)))
        if edit_form.is_valid():
            edit_form.save(request=request)
            return redirect(reverse('restaurantAdmin'))

    return render(request, "restaurant__adminEdit.html", {"form": edit_form, "restaurant": restaurant})

def restaurantAdminOrderItem(request, restaurant_name, order_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    try:
        order = models.Order.objects.get(id=order_id)
    except models.Order.DoesNotExist:
        raise Http404('Order does not exist')
    sum_cost = models.Order.objects.get_sum_cost_by_id(order_id)
    return render(request, "restaurant__admin-orderItem.html", {"order": order, "sum_cost": sum_cost, "restaurant": restaurant})

def restaurantReviewsAdd(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    if request.method == 'POST':
        add_form = app.forms.ReviewForm(request.user, request.POST)
        if add_form.is_valid():
            add_form.save(restaurant_name)
            return redirect(reverse('restaurantReviews', args=(restaurant_name, )))
    else:
        add_form = app.forms.ReviewForm(request.user)
    return render(request, 'restaurant__reviewsAdd.html', {'form': add_form, "restaurant": restaurant})

def restaurantAdminMenu(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    return render(request, "restaurant__admin-menu.html", context={"restaurant": restaurant})

def restaurantAdminMenuEdit(request, restaurant_name, dish_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    choices = [(choice, choice) for choice in models.Restaurant.objects.all()]
    try:
        dish = models.Dish.objects.get(id=dish_id)
    except models.Dish.DoesNotExist:
        raise Http404('Dish does not exist')
    
    dict = model_to_dict(models.Dish.objects.get(id=dish_id))
    dict["restaurant"] = restaurant_name

    if request.method == 'GET':
        edit_form = app.forms.DishEditForm(choices, initial=dict)
    if request.method == 'POST':
        edit_form = app.forms.DishEditForm(choices, request.POST, request.FILES, instance=models.Dish.objects.get(id=dish_id), initial=dict)
        if edit_form.is_valid():
            edit_form.save(restaurant_name, request)
            return redirect(reverse('restaurantAdminMenu', args=(restaurant_name, )))
        else:
            print(edit_form.errors)

    return render(request, "restaurant__admin-menuEdit.html", {"dish": dish, "form": edit_form, "restaurant": restaurant})

def restaurantAdminMenuAdd(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    choices = [(choice, choice) for choice in models.Restaurant.objects.all()]
    if request.method == 'GET':
        add_form = app.forms.DishAddForm(choices)
    if request.method == 'POST':
        add_form = app.forms.DishAddForm(choices, request.POST, request.FILES)
        if add_form.is_valid():
            dish = add_form.save(restaurant_name, request)
            if dish:
                return redirect(reverse('restaurantAdminMenu', args=(restaurant_name, )))
            else:
                add_form.add_error(None, 'Error with creating a new dish!')
    return render(request, 'restaurant__admin-menuAdd.html', {'form': add_form, "restaurant": restaurant})

def restaurantAdminMenuDelete(request, restaurant_name, dish_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    try:
        dish = models.Dish.objects.get(id=dish_id)
    except models.Dish.DoesNotExist:
        raise Http404('Dish does not exist')
    dish.delete()
    return redirect(reverse('restaurantAdminMenu', args=(restaurant_name, )))

def restaurantAdminOrders(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    orders = paginate(request, models.Order.objects.get_all_by_restaurant(restaurant_name))['items']
    page_obj = paginate(request, models.Order.objects.get_all_by_restaurant(restaurant_name))['obj']
    num_pages = paginate(request, models.Order.objects.get_all_by_restaurant(restaurant_name))['num']
    return render(request, "restaurant__admin-orders.html", context={"orders": orders, "page_obj": page_obj, "num_pages": num_pages, "restaurant": restaurant})

def restaurantAdminReservations(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    reservations = Reservation.objects.get_all_by_restaurant(restaurant_name)
    sum_guests = models.Reservation.objects.get_sum_guests_by_restaurant(restaurant_name)
    return render(request, "restaurant__admin-reservations.html", {"reservations": reservations, "sum_guests": sum_guests, "restaurant": restaurant})

def restaurantAdminReservationsEdit(request, restaurant_name, reservation_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    try:
        reservation = models.Reservation.objects.get(id=reservation_id)
    except models.Reservation.DoesNotExist:
        raise Http404('Reservation does not exist')

    if request.method == 'GET':
        edit_form = app.forms.ReservationEditForm(initial=model_to_dict(models.Reservation.objects.get(id=reservation_id)))
    if request.method == 'POST':
        edit_form = app.forms.ReservationEditForm(request.POST, instance=models.Reservation.objects.get(id=reservation_id), initial=model_to_dict(models.Reservation.objects.get(id=reservation_id)))
        if edit_form.is_valid():
            edit_form.save(restaurant_name=restaurant_name)
            return redirect(reverse('restaurantAdminReservations', args=(restaurant_name, )))

    return render(request, "restaurant__admin-reservationsEdit.html", {"reservation": reservation, "form": edit_form, "restaurant": restaurant})

def restaurantAdminReservationsAdd(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    if request.method == 'GET':
        add_form = app.forms.ReservationAddForm()
    if request.method == 'POST':
        add_form = app.forms.ReservationAddForm(request.POST)
        if add_form.is_valid():
            reservation = add_form.save(restaurant_name=restaurant_name)
            if reservation:
                return redirect(reverse('restaurantAdminReservations', args=(restaurant_name, )))
            else:
                add_form.add_error(None, 'Error with creating a new reservation!')
    return render(request, 'restaurant__admin-reservationsAdd.html', {'form': add_form, "restaurant": restaurant})

def restaurantAdminReservationsDelete(request, restaurant_name, reservation_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    try:
        reservation = models.Reservation.objects.get(id=reservation_id)
    except models.Reservation.DoesNotExist:
        raise Http404('Reservation does not exist')
    reservation.delete()
    return redirect(reverse('restaurantAdminReservations', args=(restaurant_name, )))

def restaurantAdminReviews(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    reviews = paginate(request, models.Review.objects.get_all_by_restaurant(restaurant_name))['items']
    page_obj = paginate(request, models.Review.objects.get_all_by_restaurant(restaurant_name))['obj']
    num_pages = paginate(request, models.Review.objects.get_all_by_restaurant(restaurant_name))['num']
    return render(request, "restaurant__admin-reviews.html", context={"reviews": reviews, "page_obj": page_obj, "num_pages": num_pages, "restaurant": restaurant})

def restaurantAdminStaff(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    return render(request, "restaurant__admin-staff.html", context={"restaurant": restaurant})

def restaurantAdminStaffEdit(request, restaurant_name, worker_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0] 
    try:
        worker = models.Worker.objects.get(id=worker_id)
    except models.Worker.DoesNotExist:
        raise Http404('Worker does not exist')

    dict = model_to_dict(models.Worker.objects.get(id=worker_id))
    dict["username"] = models.Profile.objects.get(id=dict["profile"]).user.username
    choices = [(choice, choice) for choice in models.Restaurant.objects.all()]
    if request.method == 'GET':
        edit_form = app.forms.WorkerEditForm(choices, initial=dict)
    if request.method == 'POST':
        edit_form = app.forms.WorkerEditForm(choices, request.POST, request.FILES, instance=models.Worker.objects.get(id=worker_id), initial=dict)
        if edit_form.is_valid():
            edit_form.save(restaurant_name, request)
            return redirect(reverse('restaurantAdminStaff', args=(restaurant_name, )))

    return render(request, "restaurant__admin-staffEdit.html", {"worker": worker, "form": edit_form, "restaurant": restaurant})

def restaurantAdminStaffAdd(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    choices = [(choice, choice) for choice in models.Restaurant.objects.all()]
    if request.method == 'GET':
        add_form = app.forms.WorkerAddForm(choices)
    if request.method == 'POST':
        add_form = app.forms.WorkerAddForm(choices, request.POST, request.FILES)
        if add_form.is_valid():
            worker = add_form.save(restaurant_name, request)
            if worker:
                return redirect(reverse('restaurantAdminStaff', args=(restaurant_name, )))
            else:
                add_form.add_error(None, 'Error with creating a new worker!')
    return render(request, 'restaurant__admin-staffAdd.html', {'form': add_form, "restaurant": restaurant})

def restaurantAdminStaffDelete(request, restaurant_name, worker_id): 
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    try:
        worker = models.Worker.objects.get(id=worker_id)
    except models.Worker.DoesNotExist:
        raise Http404('Worker does not exist')
    profile = worker.profile
    user = worker.profile.user
    worker.delete()
    profile.delete()
    user.delete()
    
    return redirect(reverse('restaurantAdminStaff', args=(restaurant_name, )))

def restaurantAdminSupplies(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    supplies = models.Supply.objects.get_all_by_restaurant(restaurant_name)
    sum_cost = models.Supply.objects.get_sum_cost_by_restaurant(restaurant_name)
    return render(request, "restaurant__admin-supplies.html", {"supplies": supplies, "sum_cost": sum_cost, "restaurant": restaurant})

def restaurantAdminSuppliesEdit(request, restaurant_name, supply_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    try:
        supply = models.Supply.objects.get(id=supply_id)
    except models.Supply.DoesNotExist:
        raise Http404('Supply does not exist')

    if request.method == 'GET':
        edit_form = app.forms.SupplyEditForm(initial=model_to_dict(models.Supply.objects.get(id=supply_id)))
    if request.method == 'POST':
        edit_form = app.forms.SupplyEditForm(request.POST, instance=models.Supply.objects.get(id=supply_id), initial=model_to_dict(models.Supply.objects.get(id=supply_id)))
        if edit_form.is_valid():
            edit_form.save(restaurant_name, request)
            return redirect(reverse('restaurantAdminSupplies', args=(restaurant_name, )))

    return render(request, "restaurant__admin-suppliesEdit.html", {"supply": supply, "form": edit_form, "restaurant": restaurant})

def restaurantAdminSuppliesAdd(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    if request.method == 'GET':
        add_form = app.forms.SupplyAddForm()
    if request.method == 'POST':
        add_form = app.forms.SupplyAddForm(request.POST)
        if add_form.is_valid():
            supply = add_form.save(restaurant_name, request)
            if supply:
                return redirect(reverse('restaurantAdminSupplies', args=(restaurant_name, )))
            else:
                add_form.add_error(None, 'Error with creating a new supply!')
    return render(request, 'restaurant__admin-suppliesAdd.html', {'form': add_form, "restaurant": restaurant})

def restaurantAdminSuppliesDelete(request, restaurant_name, supply_id):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    try:
        supply = models.Supply.objects.get(id=supply_id)
    except models.Supply.DoesNotExist:
        raise Http404('Supply does not exist')
    supply.delete()
    return redirect(reverse('restaurantAdminSupplies', args=(restaurant_name, )))

def restaurantAdminProfit(request, restaurant_name):
    restaurant = models.Restaurant.objects.get_by_name(restaurant_name)[0]
    revenues = calculate_profit(restaurant_name)
    sum_profit = models.Revenue.objects.get_sum_profit_by_current_month_and_restaurant(restaurant_name)
    return render(request, "restaurant__admin-profit.html", {'revenues': revenues, "sum_profit": sum_profit, "restaurant": restaurant})

def logout(request):
    auth.logout(request)
    return redirect(reverse('main'))

def login(request):   
    if request.method == "POST":
        login_form = app.forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('main'))
            else:
                login_form.add_error(None, "Wrong username or password!")
    else:
        login_form = app.forms.LoginForm()
                
    return render(request, 'login.html', {'form': login_form})

@login_required(login_url="login")
def profile(request):
    if request.method == 'GET':
        edit_form = app.forms.ProfileForm(initial=model_to_dict(request.user))
    if request.method == 'POST':
        edit_form = app.forms.ProfileForm(request.POST, request.FILES, instance=request.user, initial=model_to_dict(request.user))
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('main'))

    return render(request, 'profile.html', {'form': edit_form})

def register(request):
    if request.method == 'GET':
        user_form = app.forms.RegisterForm()
    if request.method == 'POST':
        user_form = app.forms.RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                auth.login(request, user)
                return redirect(reverse('main'))
            else:
                user_form.add_error(None, 'Error with creating a new account!')
    return render(request, 'register.html', {'form': user_form})