from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F, Min, Max
from datetime import date, timedelta, time
from django.utils import timezone
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
    
class ProfileManager(models.Manager):

    pass

class ReservationManager(models.Manager):
    def get_sum_guests_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).aggregate(total=Sum('guests'), default=0)['total']

class OrderManager(models.Manager):

    def get_all_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant)
    
    def get_new_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).order_by('-date')[:15]
    
    def get_all_by_user(self, user):
        return self.filter(profile__profile = user).order_by('-date')
    
    def get_sum_cost_by_id(self, order_id):
        return self.get(id=order_id).dishes.all().aggregate(total=Sum(F('price') * F('quantity')))['total']

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

class SupplyManager(models.Manager):

    def get_all_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant)
    
    def get_sum_cost_by_restaurant(self, restaurant):
        return self.filter(restaurant__name=restaurant).aggregate(total=Sum(F('price') * F('weight'), default=0))['total']

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
    #restaurant = models.ForeignKey('Restaurant', blank=True,  null=True, on_delete=models.PROTECT)

    objects = ReservationManager()


class Profile(models.Model):
    profile = models.OneToOneField(User, null=True, on_delete=models.PROTECT, default="")
    avatar = models.ImageField(null=True, blank=True, default="avatar.png", upload_to="avatar/%Y/%M/%D")

    def __str__(self):
        return f'Profile: {self.profile}'
    
    objects = ProfileManager()
    

class Restaurant(models.Model):
    name = models.CharField(blank=False, max_length=32, default="")
    address = models.CharField(blank=False, max_length=50)
    phone_regex = RegexValidator(regex=r'^\+?[7,8]?[\s,-]?\(?\d{3}\)?[\s,-]?\d{3}[\s,-]?\d{2}[\s,-]?\d{2}$', message="Invalid format")        
    phone = models.CharField(validators=[phone_regex], max_length=12, null=True)          

    objects = RestaurantManager()

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.PROTECT, blank=True, null=True, default="")
    table = models.IntegerField(blank=False, null=True, default=1)
    guests = models.IntegerField(blank=False, null=True, default=1)
    date = models.DateTimeField(blank=False, null=True)
    dishes = models.ManyToManyField('Dish', blank=True)
    restaurant = models.ForeignKey('Restaurant', blank=True, on_delete=models.PROTECT)
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
        ('Супы', 'Супы'),
    )
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='sections',
    )
    name = models.CharField(choices=SECTION_CHOICES, max_length=10, blank=False, default="")

    def __str__(self):
        return f'{self.name}, {self.menu.restaurant.name}'

class Dish(models.Model):
    name = models.CharField(blank=False, max_length=32)
    content = models.TextField(blank=False, max_length=32)
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='dishes',
    )
    price = models.IntegerField()
    weight = models.IntegerField()
    quantity = models.IntegerField(default=1)
    img = models.ImageField(null=True, blank=True, default="dish.webp", upload_to="dish_image/%Y/%M/%D")

    objects = DishManager()

    def __str__(self):
        return f'{self.name} x{self.quantity}'

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

    def __str__(self):
        return f'{self.name}, {self.restaurant.name}'

class Worker(models.Model):

    name = models.CharField(blank=False, max_length=32)
    profession = models.ForeignKey(
        Profession,
        on_delete=models.CASCADE,
        related_name='workers',
        default=""
    )
    salary = models.IntegerField()
    avatar = models.ImageField(null=True, blank=True, default="worker.jpeg", upload_to="avatar/%Y/%M/%D")

    objects = WorkerManager()

    def __str__(self):
        return f'Worker: {self.name}'

class Supply(models.Model):
    name = models.CharField(blank=False, max_length=32)
    provider = models.CharField(blank=False, max_length=32)
    restaurant = models.ForeignKey('Restaurant', blank=True,  null=True, on_delete=models.PROTECT)
    price = models.IntegerField()
    weight = models.IntegerField()

    objects = SupplyManager()

    


    


