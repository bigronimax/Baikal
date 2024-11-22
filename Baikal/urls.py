from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('adminDjango/', admin.site.urls),
    path("main", views.main, name="main"),
    path("main/<str:restaurant_name>", views.restaurantIndex, name="restaurantIndex"),
    path("main/<str:restaurant_name>/reservation", views.restaurantReservation, name="restaurantReservation"),
    path("main/<str:restaurant_name>/menu", views.restaurantMenu, name="restaurantMenu"),
    path('main/<str:restaurant_name>/', include('cart.urls')),

    path("main/<str:restaurant_name>/reviews", views.restaurantReviews, name="restaurantReviews"),
    path("main/<str:restaurant_name>/reviews/add", views.restaurantReviewsAdd, name="restaurantReviewsAdd"),

    path("main/<str:restaurant_name>/orders", views.restaurantOrders, name="restaurantOrders"),
    path("main/<str:restaurant_name>/orders/<int:order_id>", views.restaurantOrderItem, name="restaurantOrderItem"),

    path("profile", views.profile, name="profile"),
    path("login", views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path("register", views.register, name="register"),

    path("main/<str:restaurant_name>/admin/menu", views.restaurantAdminMenu, name="restaurantAdminMenu"),
    path("main/<str:restaurant_name>/admin/menu/add", views.restaurantAdminMenuAdd, name="restaurantAdminMenuAdd"),
    path("main/<str:restaurant_name>/admin/menu/delete/<int:dish_id>", views.restaurantAdminMenuDelete, name="restaurantAdminMenuDelete"),
    path("main/<str:restaurant_name>/admin/menu/<int:dish_id>", views.restaurantAdminMenuEdit, name="restaurantAdminMenuEdit"),

    path("main/<str:restaurant_name>/admin/orders", views.restaurantAdminOrders, name="restaurantAdminOrders"),
    path("main/<str:restaurant_name>/admin/orders/<int:order_id>", views.restaurantAdminOrderItem, name="restaurantAdminOrderItem"),

    path("main/<str:restaurant_name>/admin/reviews", views.restaurantAdminReviews, name="restaurantAdminReviews"),

    path("main/<str:restaurant_name>/admin/staff", views.restaurantAdminStaff, name="restaurantAdminStaff"),
    path("main/<str:restaurant_name>/admin/staff/add", views.restaurantAdminStaffAdd, name="restaurantAdminStaffAdd"),
    path("main/<str:restaurant_name>/admin/staff/delete/<int:worker_id>", views.restaurantAdminStaffDelete, name="restaurantAdminStaffDelete"),
    path("main/<str:restaurant_name>/admin/staff/<int:worker_id>", views.restaurantAdminStaffEdit, name="restaurantAdminStaffEdit"),

    path("main/<str:restaurant_name>/admin/reservations", views.restaurantAdminReservations, name="restaurantAdminReservations"),
    path("main/<str:restaurant_name>/admin/reservations/add", views.restaurantAdminReservationsAdd, name="restaurantAdminReservationsAdd"),
    path("main/<str:restaurant_name>/admin/reservations/delete/<int:reservation_id>", views.restaurantAdminReservationsDelete, name="restaurantAdminReservationsDelete"),
    path("main/<str:restaurant_name>/admin/reservations/<int:reservation_id>", views.restaurantAdminReservationsEdit, name="restaurantAdminReservationsEdit"),

    path("main/<str:restaurant_name>/admin/profit", views.restaurantAdminProfit, name="restaurantAdminProfit"),

    path("main/<str:restaurant_name>/admin/supplies", views.restaurantAdminSupplies, name="restaurantAdminSupplies"),
    path("main/<str:restaurant_name>/admin/supplies/add", views.restaurantAdminSuppliesAdd, name="restaurantAdminSuppliesAdd"),
    path("main/<str:restaurant_name>/admin/supplies/delete/<int:supply_id>", views.restaurantAdminSuppliesDelete, name="restaurantAdminSuppliesDelete"),
    path("main/<str:restaurant_name>/admin/supplies/<int:supply_id>", views.restaurantAdminSuppliesEdit, name="restaurantAdminSuppliesEdit"),

    path("admin", views.restaurantAdmin, name="restaurantAdmin"),
    path("main/<str:restaurant_name>/admin", views.restaurantAdminEdit, name="restaurantAdminEdit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
