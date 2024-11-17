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

def paginate(request, objects, per_page=3):
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_items = paginator.page(page_number)
    num_pages = paginator.num_pages
    return {'items': page_items, 'obj': page_obj, 'num': num_pages}

def redirect_continue(request):
    continue_href = request.GET.get('continue', '/')
    return redirect(continue_href)

def main(request):
    return render(request, "main.html")

def hunterIndex(request):
    return render(request, "hunter__index.html")

def hunterReservation(request):
    if request.method == 'POST':
        reservation_form = app.forms.ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation_form.save()
            return redirect(reverse('hunterIndex'))
    else:
        reservation_form = app.forms.ReservationForm()
        
    return render(request, "hunter__reservation.html", {'form': reservation_form})

def hunterMenu(request):
    restaurant = models.Restaurant.objects.get_by_name("Hunter")[0]
    return render(request, "hunter__menu.html", context={"restaurant": restaurant})

def hunterReviews(request):
    reviews = paginate(request, models.Review.objects.get_new_by_restaurant("Hunter"))['items']
    page_obj = paginate(request, models.Review.objects.get_new_by_restaurant("Hunter"))['obj']
    num_pages = paginate(request, models.Review.objects.get_new_by_restaurant("Hunter"))['num']
    return render(request, "hunter__reviews.html", context={"reviews": reviews, "page_obj": page_obj, "num_pages": num_pages})

@login_required(login_url="login", redirect_field_name="continue")
def hunterOrders(request):
    orders = paginate(request, models.Order.objects.get_all_by_user(request.user))['items']
    page_obj = paginate(request, models.Order.objects.get_all_by_user(request.user))['obj']
    num_pages = paginate(request, models.Order.objects.get_all_by_user(request.user))['num']
    return render(request, "hunter__orders.html", context={"orders": orders, "page_obj": page_obj, "num_pages": num_pages})

def hunterOrderItem(request, order_id):
    try:
        order = models.Order.objects.get(id=order_id)
    except models.Order.DoesNotExist:
        raise Http404('Order does not exist')
    sum_cost = models.Order.objects.get_sum_cost_by_id(order_id)
    return render(request, "hunter__orderItem.html", {"order": order, "sum_cost": sum_cost})

def hunterAdminOrderItem(request, order_id):
    try:
        order = models.Order.objects.get(id=order_id)
    except models.Order.DoesNotExist:
        raise Http404('Order does not exist')
    sum_cost = models.Order.objects.get_sum_cost_by_id(order_id)
    return render(request, "hunter__admin-orderItem.html", {"order": order, "sum_cost": sum_cost})

def hunterReviewsAdd(request):
    if request.method == 'POST':
        add_form = app.forms.ReviewForm(request.user, request.POST)
        if add_form.is_valid():
            add_form.save("Hunter")
            return redirect(reverse('hunterReviews'))
    else:
        add_form = app.forms.ReviewForm(request.user)
    return render(request, 'hunter__reviewsAdd.html', {'form': add_form})

def hunterAdminMenu(request):
    restaurant = models.Restaurant.objects.get_by_name("Hunter")[0]
    return render(request, "hunter__admin-menu.html", context={"restaurant": restaurant})

def hunterAdminMenuEdit(request, dish_id):
    try:
        dish = models.Dish.objects.get(id=dish_id)
    except models.Dish.DoesNotExist:
        raise Http404('Dish does not exist')

    if request.method == 'GET':
        edit_form = app.forms.DishForm(initial=model_to_dict(models.Dish.objects.get(id=dish_id)))
    if request.method == 'POST':
        edit_form = app.forms.DishForm(request.POST, request.FILES, instance=models.Dish.objects.get(id=dish_id), initial=model_to_dict(models.Dish.objects.get(id=dish_id)))
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('hunterAdminMenu'))

    return render(request, "hunter__admin-menuEdit.html", {"dish": dish, "form": edit_form})

def hunterAdminMenuAdd(request):
    if request.method == 'GET':
        add_form = app.forms.DishForm()
    if request.method == 'POST':
        add_form = app.forms.DishForm(request.POST, request.FILES)
        if add_form.is_valid():
            dish = add_form.save()
            if dish:
                return redirect(reverse('hunterAdminMenu'))
            else:
                add_form.add_error(None, 'Error with creating a new dish!')
    return render(request, 'hunter__admin-menuAdd.html', {'form': add_form})

def hunterAdminMenuDelete(request, dish_id):
    try:
        dish = models.Dish.objects.get(id=dish_id)
    except models.Dish.DoesNotExist:
        raise Http404('Dish does not exist')
    dish.delete()
    return redirect(reverse('hunterAdminMenu'))

def hunterAdminOrders(request):
    orders = paginate(request, models.Order.objects.get_all_by_restaurant("Hunter"))['items']
    page_obj = paginate(request, models.Order.objects.get_all_by_restaurant("Hunter"))['obj']
    num_pages = paginate(request, models.Order.objects.get_all_by_restaurant("Hunter"))['num']
    return render(request, "hunter__admin-orders.html", context={"orders": orders, "page_obj": page_obj, "num_pages": num_pages})

def hunterAdminReservations(request):
    reservations = Reservation.objects.all()
    #sum_guests = models.Reservation.objects.get_sum_guests_by_restaurant("Hunter")
    return render(request, "hunter__admin-reservations.html", {"reservations": reservations})

def hunterAdminReservationsEdit(request, reservation_id):
    try:
        reservation = models.Reservation.objects.get(id=reservation_id)
    except models.Reservation.DoesNotExist:
        raise Http404('Reservation does not exist')

    if request.method == 'GET':
        edit_form = app.forms.ReservationForm(initial=model_to_dict(models.Reservation.objects.get(id=reservation_id)))
    if request.method == 'POST':
        edit_form = app.forms.ReservationForm(request.POST, instance=models.Reservation.objects.get(id=reservation_id), initial=model_to_dict(models.Reservation.objects.get(id=reservation_id)))
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('hunterAdminReservations'))

    return render(request, "hunter__admin-reservationsEdit.html", {"reservation": reservation, "form": edit_form})

def hunterAdminReservationsAdd(request):
    if request.method == 'GET':
        add_form = app.forms.ReservationForm()
    if request.method == 'POST':
        add_form = app.forms.ReservationForm(request.POST)
        if add_form.is_valid():
            reservation = add_form.save()
            if reservation:
                return redirect(reverse('hunterAdminReservations'))
            else:
                add_form.add_error(None, 'Error with creating a new reservation!')
    return render(request, 'hunter__admin-reservationsAdd.html', {'form': add_form})

def hunterAdminReservationsDelete(request, reservation_id):
    try:
        reservation = models.Reservation.objects.get(id=reservation_id)
    except models.Reservation.DoesNotExist:
        raise Http404('Reservation does not exist')
    reservation.delete()
    return redirect(reverse('hunterAdminReservations'))

def hunterAdminReviews(request):
    reviews = paginate(request, models.Review.objects.get_all_by_restaurant("Hunter"))['items']
    page_obj = paginate(request, models.Review.objects.get_all_by_restaurant("Hunter"))['obj']
    num_pages = paginate(request, models.Review.objects.get_all_by_restaurant("Hunter"))['num']
    return render(request, "hunter__admin-reviews.html", context={"reviews": reviews, "page_obj": page_obj, "num_pages": num_pages})

def hunterAdminStaff(request):
    restaurant = models.Restaurant.objects.get_by_name("Hunter")[0]
    return render(request, "hunter__admin-staff.html", context={"restaurant": restaurant})

def hunterAdminStaffEdit(request, worker_id): 
    try:
        worker = models.Worker.objects.get(id=worker_id)
    except models.Worker.DoesNotExist:
        raise Http404('Worker does not exist')

    if request.method == 'GET':
        edit_form = app.forms.WorkerForm(initial=model_to_dict(models.Worker.objects.get(id=worker_id)))
    if request.method == 'POST':
        edit_form = app.forms.WorkerForm(request.POST, request.FILES, instance=models.Worker.objects.get(id=worker_id), initial=model_to_dict(models.Worker.objects.get(id=worker_id)))
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('hunterAdminStaff'))

    return render(request, "hunter__admin-staffEdit.html", {"worker": worker, "form": edit_form})

def hunterAdminStaffAdd(request):
    if request.method == 'GET':
        add_form = app.forms.WorkerForm()
    if request.method == 'POST':
        add_form = app.forms.WorkerForm(request.POST, request.FILES)
        if add_form.is_valid():
            worker = add_form.save()
            if worker:
                return redirect(reverse('hunterAdminStaff'))
            else:
                add_form.add_error(None, 'Error with creating a new worker!')
    return render(request, 'hunter__admin-staffAdd.html', {'form': add_form})

def hunterAdminStaffDelete(request, worker_id): 
    try:
        worker = models.Worker.objects.get(id=worker_id)
    except models.Worker.DoesNotExist:
        raise Http404('Worker does not exist')
    worker.delete()
    return redirect(reverse('hunterAdminStaff'))

def hunterAdminSupplies(request):
    supplies = models.Supply.objects.get_all_by_restaurant("Hunter")
    sum_cost = models.Supply.objects.get_sum_cost_by_restaurant("Hunter")
    return render(request, "hunter__admin-supplies.html", {"supplies": supplies, "sum_cost": sum_cost})

def hunterAdminSuppliesEdit(request, supply_id):
    try:
        supply = models.Supply.objects.get(id=supply_id)
    except models.Supply.DoesNotExist:
        raise Http404('Supply does not exist')

    if request.method == 'GET':
        edit_form = app.forms.SupplyForm(initial=model_to_dict(models.Supply.objects.get(id=supply_id)))
    if request.method == 'POST':
        edit_form = app.forms.SupplyForm(request.POST, instance=models.Supply.objects.get(id=supply_id), initial=model_to_dict(models.Supply.objects.get(id=supply_id)))
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('hunterAdminSupplies'))

    return render(request, "hunter__admin-suppliesEdit.html", {"supply": supply, "form": edit_form})

def hunterAdminSuppliesAdd(request):
    if request.method == 'GET':
        add_form = app.forms.SupplyForm()
    if request.method == 'POST':
        add_form = app.forms.SupplyForm(request.POST)
        if add_form.is_valid():
            supply = add_form.save()
            if supply:
                return redirect(reverse('hunterAdminSupplies'))
            else:
                add_form.add_error(None, 'Error with creating a new supply!')
    return render(request, 'hunter__admin-suppliesAdd.html', {'form': add_form})

def hunterAdminSuppliesDelete(request, supply_id):
    print("AAA")
    try:
        supply = models.Supply.objects.get(id=supply_id)
    except models.Supply.DoesNotExist:
        raise Http404('Supply does not exist')
    print("BBB")
    supply.delete()
    return redirect(reverse('hunterAdminSupplies'))

def hunterAdminProfit(request):
    return render(request, "hunter__admin-profit.html")

def logout(request):
    auth.logout(request)
    return redirect(request.GET.get("continue", "main"))

def login(request):   
    if request.method == "POST":
        login_form = app.forms.LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get("continue", "main"))
            else:
                login_form.add_error(None, "Wrong username or password!")
    else:
        login_form = app.forms.LoginForm()
                
    return render(request, 'login.html', {'form': login_form})

@login_required(login_url="login", redirect_field_name="continue")
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