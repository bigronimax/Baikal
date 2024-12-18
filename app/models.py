from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F, Min, Max
from datetime import date, timedelta, time
from django.utils import timezone
from calendar import monthrange
from django.core.validators import RegexValidator

# Create your models here.

class ReviewManager(models.Manager):

    def get_all_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant)
    
    def get_new_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).order_by('-date')[:15]
    
class RestaurantManager(models.Manager):

    def get_by_name(self, _name):
        return self.filter(name = _name)
    

class ReservationManager(models.Manager):

    def get_all_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant)

    def get_sum_guests_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).aggregate(total=Sum("guests", default=0))['total']
       
    
class OrderManager(models.Manager):

    def get_all_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant)
    
    def get_new_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).order_by('-date')[:15]
    
    def get_all_by_user_and_restaurant(self, user, restaurant):
        return self.filter(profile__user = user).filter(restaurant__name=restaurant).order_by('-date')
    
    def get_sum_cost_by_id(self, order_id):
        return self.filter(id=order_id).aggregate(total=Sum(F('dishes__dish__price') * F('dishes__quantity')))['total']
    
    def get_sum_cost_by_restaurant_date(self, restaurant, date):
        return self.filter(restaurant__name=restaurant).filter(date__date=date).aggregate(total=Sum(F('dishes__dish__price') * F('dishes__quantity'), default=0))['total']
    
    def get_sum_guests_by_restaurant_date(self, restaurant, date):
        return self.filter(restaurant__name=restaurant).filter(date__date=date).aggregate(total=Sum("guests", default=0))['total']
    

class DishManager(models.Manager):

    def get_restaurant(self, restaurant):
        return self.filter(section__menu__restaurant__name = restaurant)
    
    def get_popular_dishes(self):
        return self.annotate(num_dish = Count('order')).order_by('-num_dish')[:5]
    
class MenuManager(models.Manager):

    def get_restaurant(self, restaurant):
        return self.filter(restaurant__name = restaurant)
    
class WorkerManager(models.Manager):

    def get_profession(self, _profession):
        return super().get_queryset().filter(profession__name = _profession)

    def get_highly_paid_waiters(self):
        return self.order_by('salary')
    
    def get_sum_cost_by_restaurant(self, restaurant):
        return self.filter(profession__restaurant__name=restaurant).aggregate(total=Sum("salary", default=0))['total']

class SupplyManager(models.Manager):

    def get_all_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant)
    
    def get_sum_cost_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).aggregate(total=Sum(F('price') * F('weight'), default=0))['total']
    
class RevenueManager(models.Manager):

    def get_by_current_month_and_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).filter(date__range=(
            date(date.today().year, date.today().month, 1), 
            date(date.today().year, date.today().month, monthrange(date.today().year, date.today().month)[1])
        ))
    
    def get_sum_profit_by_current_month_and_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).filter(date__range=(
            date(date.today().year, date.today().month, 1), 
            date(date.today().year, date.today().month, monthrange(date.today().year, date.today().month)[1])
        )).aggregate(total=Sum("profit", default=0))['total']

class SectionManager(models.Manager):

    def get_by_name_and_restaurant(self, name, restaurant):
        return self.filter(menu__restaurant__name=restaurant).filter(name=name)

class ProfessionManager(models.Manager):

    def get_by_name_and_restaurant(self, name, restaurant):
        return self.filter(restaurant__name=restaurant).filter(name=name)

class Review(models.Model):
    
    RATING_CHOICES = (
        ('Удивительно!', 'Удивительно!'),
        ('Хорошо!', 'Хорошо!'),
        ('Плохо!', 'Плохо!'),
        ('Ужасно!', 'Ужасно!'),
    )

    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False, max_length=200)
    date = models.DateTimeField(blank=False, null=True)
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, blank=True, null=True, default="")
    restaurant = models.ForeignKey('Restaurant', blank=True,  null=True, on_delete=models.PROTECT)
    verdict = models.CharField(choices=RATING_CHOICES, max_length=15, default="")
    
    objects = ReviewManager()

    def __str__(self):
        return f'Review: {self.title}'

class Reservation(models.Model):
    GUESTS_CHOICES = (
        (1, '1 гость'),
        (2, '2 Гостя'),
        (3, '3 Гостя'),
        (4, '4 Гостя'),
        (5, '5 Гостей'),
        (6, '6 Гостей'),
    )
    HOUR_CHOICES = [(time(hour=x), '{:02d}:00'.format(x)) for x in range(10, 23)]

    name = models.CharField(max_length=20, blank=False)
    phone_regex = RegexValidator(regex=r'^\+?[7,8]?[\s,-]?\(?\d{3}\)?[\s,-]?\d{3}[\s,-]?\d{2}[\s,-]?\d{2}$', message="Invalid format")        
    phone = models.CharField(validators=[phone_regex], max_length=12, null=False, blank=False, unique=True)
    guests = models.IntegerField(choices=GUESTS_CHOICES, blank=False, default="")
    date = models.DateField(blank=False, default=timezone.now().date())
    time = models.TimeField(choices=HOUR_CHOICES, blank=False, default="")
    comment = models.TextField(max_length=100, null=True, blank=True)
    restaurant = models.ForeignKey('Restaurant', blank=False,  null=False, on_delete=models.PROTECT, default="")

    objects = ReservationManager()


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.PROTECT, related_name='profile', default="")
    avatar = models.ImageField(null=True, blank=True, default="avatar.png", upload_to="avatar/%Y/%M/%D")

    def __str__(self):
        return f'Profile: {self.user}'
    
    

class Restaurant(models.Model):
    name = models.CharField(blank=False, max_length=32, default="")
    content = models.TextField(blank=False, max_length=200, default="")
    address = models.CharField(blank=False, max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?[7,8]?[\s,-]?\(?\d{3}\)?[\s,-]?\d{3}[\s,-]?\d{2}[\s,-]?\d{2}$', message="Invalid format")        
    phone = models.CharField(validators=[phone_regex], max_length=12, null=True)    
    img = models.ImageField(null=True, blank=True, default="background.jpg", upload_to="restaurant_image/%Y/%M/%D")      

    objects = RestaurantManager()

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, blank=False, null=True, default="")
    table = models.IntegerField(blank=False, null=True, default=1)
    guests = models.IntegerField(blank=False, null=True, default=1)
    date = models.DateTimeField(blank=False, null=True)
    restaurant = models.ForeignKey('Restaurant', blank=False, on_delete=models.PROTECT)
    objects = OrderManager()

    def __str__(self):
        return f'Order: {self.id}'

class Menu(models.Model):          
    restaurant = models.OneToOneField(
        Restaurant,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    objects = MenuManager()

class Section(models.Model):
    SECTION_CHOICES = (
        ('Комбо', 'Комбо'),
        ('Закуски', 'Закуски'),
        ('Горячее', 'Горячее'),
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='sections',
    )
    name = models.CharField(choices=SECTION_CHOICES, max_length=10, blank=False, default="")

    objects = SectionManager()

    def __str__(self):
        return f'{self.name}, {self.menu.restaurant.name}'

class Dish(models.Model):
    name = models.CharField(blank=False, max_length=32)
    content = models.TextField(blank=False, max_length=32)
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='dishes',
        default=""
    )
    price = models.IntegerField()
    weight = models.IntegerField()
    img = models.ImageField(null=True, blank=True, default="dish.webp", upload_to="dish_image/%Y/%M/%D")

    objects = DishManager()


class OrderDish(models.Model):
    dish = models.ForeignKey(Dish, blank=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='dishes', null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.dish.name} x{self.quantity}'

class Profession(models.Model):
    PROFESSION_CHOICES = (
        ('Официанты', 'Официанты'),
        ('Повара', 'Повара'),
        ('Менеджеры', 'Менеджеры'),
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='professions',
        default=""
    )
    name = models.CharField(choices=PROFESSION_CHOICES, max_length=10, blank=False, default="")

    objects = ProfessionManager()

    def __str__(self):
        return f'{self.name}, {self.restaurant.name}'

class Worker(models.Model):
    profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        related_name='workers',
        default=""
    )
    salary = models.IntegerField()
    profile = models.OneToOneField('Profile', on_delete=models.PROTECT, blank=True, null=True, related_name='worker', default="")

    objects = WorkerManager()

    def __str__(self):
        return f'Worker: {self.profile.user.username}'

class Supply(models.Model):
    name = models.CharField(blank=False, max_length=32)
    provider = models.CharField(blank=False, max_length=32)
    restaurant = models.ForeignKey('Restaurant', blank=False, on_delete=models.PROTECT, default="")
    price = models.IntegerField(blank=False)
    weight = models.IntegerField(blank=False)

    objects = SupplyManager()

class Revenue(models.Model):
    date = models.DateField(blank=True, null=False)
    guests = models.IntegerField(null=True)
    income = models.IntegerField(null=True)
    consumption = models.IntegerField(null=True)
    profit = models.IntegerField(null=True)
    restaurant = models.ForeignKey('Restaurant', null=True, on_delete=models.PROTECT)

    objects = RevenueManager()


    


    


