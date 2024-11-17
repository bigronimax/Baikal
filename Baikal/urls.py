from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("main", views.main, name="main"),
    path("main/hunter", views.hunterIndex, name="hunterIndex"),
    path("main/hunter/reservation", views.hunterReservation, name="hunterReservation"),
    path("main/hunter/menu", views.hunterMenu, name="hunterMenu"),
    path('main/hunter/', include('cart.urls')),

    path("main/hunter/reviews", views.hunterReviews, name="hunterReviews"),
    path("main/hunter/reviews/add", views.hunterReviewsAdd, name="hunterReviewsAdd"),

    path("main/hunter/orders", views.hunterOrders, name="hunterOrders"),
    path("main/hunter/orders/<int:order_id>", views.hunterOrderItem, name="hunterOrderItem"),

    path("main/profile", views.profile, name="profile"),
    path("main/login", views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path("main/register", views.register, name="register"),

    path("main/hunter/admin/menu", views.hunterAdminMenu, name="hunterAdminMenu"),
    path("main/hunter/admin/menu/add", views.hunterAdminMenuAdd, name="hunterAdminMenuAdd"),
    path("main/hunter/admin/menu/delete/<int:dish_id>", views.hunterAdminMenuDelete, name="hunterAdminMenuDelete"),
    path("main/hunter/admin/menu/<int:dish_id>", views.hunterAdminMenuEdit, name="hunterAdminMenuEdit"),

    path("main/hunter/admin/orders", views.hunterAdminOrders, name="hunterAdminOrders"),
    path("main/hunter/admin/orders/<int:order_id>", views.hunterAdminOrderItem, name="hunterAdminOrderItem"),

    path("main/hunter/admin/reviews", views.hunterAdminReviews, name="hunterAdminReviews"),

    path("main/hunter/admin/staff", views.hunterAdminStaff, name="hunterAdminStaff"),
    path("main/hunter/admin/staff/add", views.hunterAdminStaffAdd, name="hunterAdminStaffAdd"),
    path("main/hunter/admin/staff/delete/<int:worker_id>", views.hunterAdminStaffDelete, name="hunterAdminStaffDelete"),
    path("main/hunter/admin/staff/<int:worker_id>", views.hunterAdminStaffEdit, name="hunterAdminStaffEdit"),

    path("main/hunter/admin/reservations", views.hunterAdminReservations, name="hunterAdminReservations"),
    path("main/hunter/admin/reservations/add", views.hunterAdminReservationsAdd, name="hunterAdminReservationsAdd"),
    path("main/hunter/admin/reservations/delete/<int:reservation_id>", views.hunterAdminReservationsDelete, name="hunterAdminReservationsDelete"),
    path("main/hunter/admin/reservations/<int:reservation_id>", views.hunterAdminReservationsEdit, name="hunterAdminReservationsEdit"),

    path("main/hunter/admin/profit", views.hunterAdminProfit, name="hunterAdminProfit"),

    path("main/hunter/admin/supplies", views.hunterAdminSupplies, name="hunterAdminSupplies"),
    path("main/hunter/admin/supplies/add", views.hunterAdminSuppliesAdd, name="hunterAdminSuppliesAdd"),
    path("main/hunter/admin/supplies/delete/<int:supply_id>", views.hunterAdminSuppliesDelete, name="hunterAdminSuppliesDelete"),
    path("main/hunter/admin/supplies/<int:supply_id>", views.hunterAdminSuppliesEdit, name="hunterAdminSuppliesEdit"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
