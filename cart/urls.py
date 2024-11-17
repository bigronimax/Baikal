from django.conf import settings
from django.contrib import admin
from django.urls import path
from cart import views
from django.conf.urls.static import static

urlpatterns = [
    path("cart", views.cartSummary, name="cartSummary"),
    path("cart/add", views.cartAdd, name="cartAdd"),
    path("cart/delete", views.cartDelete, name="cartDelete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
