"""
URL configuration for Baikal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("main", views.main, name="main"),
    path("main/hunter", views.hunterIndex, name="hunterIndex"),
    path("main/hunter/reservation", views.hunterReservation, name="hunterReservation"),
    path("main/hunter/menu", views.hunterMenu, name="hunterMenu"),
    path("main/hunter/reviews", views.hunterReviews, name="hunterReviews"),

    path("main/profile", views.profile, name="profile"),
    path("main/access", views.access, name="access"),

    path("main/hunter/admin/menu", views.hunterAdminMenu, name="hunterAdminMenu"),
    path("main/hunter/admin/orders", views.hunterAdminOrders, name="hunterAdminOrders"),
    path("main/hunter/admin/reviews", views.hunterAdminReviews, name="hunterAdminReviews"),
    path("main/hunter/admin/staff", views.hunterAdminStaff, name="hunterAdminStaff"),
    path("main/hunter/admin/reservations", views.hunterAdminReservations, name="hunterAdminReservations"),
    path("main/hunter/admin/profit", views.hunterAdminProfit, name="hunterAdminProfit"),
    path("main/hunter/admin/supplies", views.hunterAdminSupplies, name="hunterAdminSupplies"),
]
