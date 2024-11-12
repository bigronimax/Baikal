from django.shortcuts import render, redirect
from . import models
from django.contrib import auth
import app.forms
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from .models import Reservation


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
            reservation = reservation_form.save()
            print(reservation)
            return redirect(reverse('hunterIndex'))
        print(reservation_form.errors)
    else:
        reservation_form = app.forms.ReservationForm()
        
    return render(request, "hunter__reservation.html", {'form': reservation_form})

def hunterMenu(request):
    restaurant = models.Restaurant.objects.get_by_name("Hunter")[0]
    print(restaurant)
    return render(request, "hunter__menu.html", context={"restaurant": restaurant})

def hunterReviews(request):
    reviews = models.paginate(request, models.Review.objects.get_new_by_restaurant("Hunter"))['items']
    page_obj = models.paginate(request, models.Review.objects.get_new_by_restaurant("Hunter"))['obj']
    return render(request, "hunter__reviews.html", context={"reviews": reviews, "page_obj": page_obj})

def hunterAdminMenu(request):
    restaurant = models.Restaurant.objects.get_by_name("Hunter")[0]
    return render(request, "hunter__admin-menu.html", context={"restaurant": restaurant})

def hunterAdminOrders(request):
    orders = models.Order.objects.get_new_orders()
    return render(request, "hunter__admin-orders.html", context={"orders": orders})

def hunterAdminReservations(request):
    reservations = Reservation.objects.all()
    return render(request, "hunter__admin-reservations.html", {"reservations": reservations})

def hunterAdminReviews(request):
    reviews = models.paginate(request, models.Review.objects.get_all_by_restaurant("Hunter"))['items']
    page_obj = models.paginate(request, models.Review.objects.get_all_by_restaurant("Hunter"))['obj']
    return render(request, "hunter__admin-reviews.html", context={"reviews": reviews, "page_obj": page_obj})

def hunterAdminStaff(request):
    restaurant = models.Restaurant.objects.get_by_name("Hunter")[0]
    return render(request, "hunter__admin-staff.html", context={"restaurant": restaurant})

def hunterAdminSupplies(request):
    return render(request, "hunter__admin-supplies.html")

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