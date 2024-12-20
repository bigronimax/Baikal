from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Review)
admin.site.register(models.Profile)
admin.site.register(models.Restaurant)
admin.site.register(models.Dish)
admin.site.register(models.Section)
admin.site.register(models.Menu)
admin.site.register(models.Profession)
admin.site.register(models.Worker)
admin.site.register(models.Order)
admin.site.register(models.Reservation)
admin.site.register(models.OrderDish)
admin.site.register(models.Revenue)
admin.site.register(models.Supply)