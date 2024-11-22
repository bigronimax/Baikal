from django import forms
from django.contrib.auth.models import User
from django.forms import ImageField, ValidationError
from django.core.validators import validate_email
from app.models import Review, Profile, Reservation, Worker, Supply, Dish, Restaurant, Section, Profession
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware
from django.contrib.auth.models import Group, Permission

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(min_length=3, label="Password", widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not(User.objects.filter(username=username).all().count()):
            raise ValidationError("Wrong username!")
        return username
    

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_check']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).all().count():
            raise ValidationError('Username is already exists!')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        if User.objects.filter(email=email).all().count():
            raise ValidationError('Email is already exists!')
        return email

    def clean(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')

        if password != password_check:
            raise ValidationError('Passwords mismatch!')
    
    def save(self):
        self.cleaned_data.pop('password_check')
        user = User.objects.create_user(**self.cleaned_data)
        Profile.objects.create(user=user)
        return user
    
class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_username(self, **kwargs):
        user = super().save(**kwargs)
        new_username = self.cleaned_data.get('username')
        if User.objects.filter(username=new_username).all().count() and new_username != user.username:
            raise ValidationError('Username is already exists!')
        return new_username
    
    def clean_email(self, **kwargs):
        user = super().save(**kwargs)
        new_email = self.cleaned_data.get('email')
        validate_email(new_email)
        if User.objects.filter(email=new_email).all().count() and new_email != user.email:
            raise ValidationError('Email is already exists!')
        return new_email
    
    def save(self, **kwargs):
        user = super().save(**kwargs)

        profile = user.profile
        received_avatar = self.cleaned_data.get('avatar')
        new_username = self.cleaned_data.get('username')
        new_email = self.cleaned_data.get('email')

        if new_username != user.username:
            user.username = new_username
            profile.save()
        if new_email != user.email:
            user.email = new_email
            profile.save()
        if received_avatar:
            profile.avatar = received_avatar
            profile.save()

        return user

class WorkerAddForm(forms.ModelForm):

    username = forms.CharField(label='Username')
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    profession = forms.ChoiceField(choices=Profession.PROFESSION_CHOICES) 
    restaurant = forms.ChoiceField(choices=())
    avatar = forms.ImageField(required=False)


    class Meta:
        model = Worker
        fields = ["salary"]
        widgets = {
            'salary': forms.TextInput(attrs={'type': 'text'}),
            'avatar': forms.FileInput(attrs={'type': 'file'}),
        }
    
    def __init__(self, choices, *args, **kwargs):
        super(WorkerAddForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].choices = choices
        self.fields['restaurant'].required = False

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).all().count():
            raise ValidationError('Username is already exists!')
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        if User.objects.filter(email=email).all().count():
            raise ValidationError('Email is already exists!')
        return email

    def clean(self):
        password = self.cleaned_data.get('password')
        password_check = self.cleaned_data.get('password_check')

        if password != password_check:
            raise ValidationError('Passwords mismatch!')
        
    def save(self, restaurant_name, request):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        salary = self.cleaned_data.get('salary')
        profession = self.cleaned_data.get('profession')
        restaurant = self.cleaned_data.get('restaurant')
        avatar = self.cleaned_data.get('avatar')

        if (not request.user.is_superuser):
            restaurant = Restaurant.objects.get_by_name(restaurant_name)[0]

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        
        Profile.objects.create(user=user)
        profile = Profile.objects.get(user=user)
        if avatar:
            profile.avatar = avatar
        profile.save()
        worker = Worker.objects.create(
            profile=profile,
            salary=salary,
            profession=Profession.objects.get_by_name_and_restaurant(profession, restaurant)[0]
        )

        profession = worker.profession
        profession.restaurant.name = restaurant
        profession.save()

        waiter_group = Group.objects.get(name='waiter')
        chef_group = Group.objects.get(name='chef')
        manager_group = Group.objects.get(name='manager')

        if worker.profession.name == "Официанты":
            worker.profile.user.groups.add(waiter_group)
            worker.profile.user.save()
            worker.save()
        elif worker.profession.name == "Повара":
            worker.profile.user.groups.add(chef_group)
            worker.profile.user.save()
            worker.save()
        elif worker.profession.name == "Менеджеры":
            worker.profile.user.groups.add(manager_group)
            worker.profile.user.save()
            worker.save()

        return worker



class WorkerEditForm(forms.ModelForm):

    profession = forms.ChoiceField(choices=Profession.PROFESSION_CHOICES) 
    restaurant = forms.ChoiceField(choices=())
    username = forms.CharField(label='Username')
    avatar = forms.ImageField(required=False)
    
    class Meta:
        model = Worker
        fields = ["salary"]
        widgets = {
            'salary': forms.TextInput(attrs={'type': 'text'}),
            'avatar': forms.FileInput(attrs={'type': 'file'}),
        }
    
    def __init__(self, choices, *args, **kwargs):
        super(WorkerEditForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].choices = choices
        self.fields['restaurant'].required = False

    def clean_username(self, **kwargs):
        worker = super().save(**kwargs)
        user = worker.profile.user
        new_username = self.cleaned_data.get('username')
        if User.objects.filter(username=new_username).all().count() and new_username != user.username:
            raise ValidationError('Username is already exists!')
        return new_username
    
    def save(self, restaurant_name, request, **kwargs):
        worker = super().save(**kwargs)

        received_avatar = self.cleaned_data.get('avatar')
        new_username = self.cleaned_data.get('username')
        new_salary = self.cleaned_data.get('salary')
        new_profession = self.cleaned_data.get('profession')
        new_restaurant = self.cleaned_data.get('restaurant')

        if (not request.user.is_superuser):
            new_restaurant = Restaurant.objects.get_by_name(restaurant_name)[0]

        profile = worker.profile
        user = worker.profile.user

        if new_username != user.username:
            user.username = new_username
            user.save()
            worker.save()
        if new_salary != worker.salary:
            worker.salary = new_salary
            worker.save()
        if received_avatar:
            profile.avatar = received_avatar
            profile.save()
            worker.save()
        
        worker.profession = Profession.objects.get_by_name_and_restaurant(new_profession, new_restaurant)[0] 
        worker.profession.save()
        worker.save()

        waiter_group = Group.objects.get(name='waiter')
        chef_group = Group.objects.get(name='chef')
        manager_group = Group.objects.get(name='manager')

        if worker.profession.name == "Официанты":
            worker.profile.user.groups.add(waiter_group)
            worker.profile.user.save()
            worker.save()
        elif worker.profession.name == "Повара":
            worker.profile.user.groups.add(chef_group)
            worker.profile.user.save()
            worker.save()
        elif worker.profession.name == "Менеджеры":
            worker.profile.user.groups.add(manager_group)
            worker.profile.user.save()
            worker.save()
        
        return worker

class SupplyAddForm(forms.ModelForm):
    
    class Meta:
        model = Supply
        fields = "__all__"
        widgets = {
            'price': forms.TextInput(attrs={'type': 'text'}),
            'weight': forms.TextInput(attrs={'type': 'text'}),
        }

    def __init__(self, *args, **kwargs):
        super(SupplyAddForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].required = False
    
    def save(self, restaurant_name, request, **kwargs):

        name = self.cleaned_data.get('name')
        provider = self.cleaned_data.get('provider')
        restaurant = self.cleaned_data.get('restaurant')
        price = self.cleaned_data.get('price')
        weight = self.cleaned_data.get('weight')

        if (not request.user.is_superuser):
            restaurant = restaurant_name

        supply = Supply.objects.create(
            name=name,
            provider=provider,
            restaurant=Restaurant.objects.get_by_name(restaurant)[0],
            price=price,
            weight=weight,
        )

        return supply

class SupplyEditForm(forms.ModelForm):
    
    class Meta:
        model = Supply
        fields = "__all__"
        widgets = {
            'price': forms.TextInput(attrs={'type': 'text'}),
            'weight': forms.TextInput(attrs={'type': 'text'}),
        }

    def __init__(self, *args, **kwargs):
        super(SupplyEditForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].required = False
    
    def save(self, restaurant_name, request, **kwargs):
        supply = super().save(**kwargs)

        new_name = self.cleaned_data.get('name')
        new_provider = self.cleaned_data.get('provider')
        new_restaurant = self.cleaned_data.get('restaurant')
        new_price = self.cleaned_data.get('price')
        new_weight = self.cleaned_data.get('weight')

        if (not request.user.is_superuser):
            new_restaurant = restaurant_name

        if new_name != supply.name:
            supply.name = new_name
            supply.save()
        if new_provider != supply.provider:
            supply.provider = new_provider
            supply.save()
        if new_restaurant != supply.restaurant.name:
            supply.restaurant = Restaurant.objects.get_by_name(new_restaurant)[0]
            supply.save()
        if new_price != supply.price:
            supply.price = new_price
            supply.save()
        if new_weight != supply.weight:
            supply.weight = new_weight
            supply.save()

        return supply
    
class DishAddForm(forms.ModelForm):
    section = forms.ChoiceField(choices=Section.SECTION_CHOICES) 
    restaurant = forms.ChoiceField(choices=())

    class Meta:
        model = Dish
        fields = ["name", "content", "price", "weight", "img"]
        widgets = {
            'price': forms.TextInput(attrs={'type': 'text'}),
            'weight': forms.TextInput(attrs={'type': 'text'}),
            'img': forms.FileInput(attrs={'type': 'file'}),
        }
    
    def __init__(self, choices, *args, **kwargs):
        super(DishAddForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].choices = choices
        self.fields['restaurant'].required = False
        
    
    def save(self, restaurant_name, request, **kwargs):

        name = self.cleaned_data.get('name')
        content = self.cleaned_data.get('content')
        section = self.cleaned_data.get('section')
        restaurant = self.cleaned_data.get('restaurant')
        price = self.cleaned_data.get('price')
        weight = self.cleaned_data.get('weight')
        received_img = self.cleaned_data.get('img')

        if (not request.user.is_superuser):
            restaurant = restaurant_name

        dish = Dish.objects.create(
            name=name,
            content=content,
            section=Section.objects.get_by_name_and_restaurant(section, restaurant)[0],
            price=price,
            weight=weight,
            img=received_img
        )

        menu = dish.section.menu
        menu.restaurant.name = restaurant
        menu.save()
        
        return dish

class DishEditForm(forms.ModelForm):
    section = forms.ChoiceField(choices=Section.SECTION_CHOICES) 
    restaurant = forms.ChoiceField(choices=())

    class Meta:
        model = Dish
        fields = ["name", "content", "price", "weight", "img"]
        widgets = {
            'price': forms.TextInput(attrs={'type': 'text'}),
            'weight': forms.TextInput(attrs={'type': 'text'}),
            'img': forms.FileInput(attrs={'type': 'file'}),
        }
    
    def __init__(self, choices, *args, **kwargs):
        super(DishEditForm, self).__init__(*args, **kwargs)
        self.fields['restaurant'].choices = choices
        self.fields['restaurant'].required = False
        
    
    def save(self, restaurant_name, request, **kwargs):
        dish = super().save(**kwargs)

        new_name = self.cleaned_data.get('name')
        new_content = self.cleaned_data.get('content')
        new_section = self.cleaned_data.get('section')
        new_restaurant = self.cleaned_data.get('restaurant')
        new_price = self.cleaned_data.get('price')
        new_weight = self.cleaned_data.get('weight')
        received_img = self.cleaned_data.get('img')

        if (not request.user.is_superuser):
            new_restaurant = restaurant_name

        if new_name != dish.name:
            dish.name = new_name
            dish.save()
        if new_content != dish.content:
            dish.content = new_content
            dish.save()
        if new_price != dish.price:
            dish.price = new_price
            dish.save()
        if new_weight != dish.weight:
            dish.weight = new_weight
            dish.save()
        if received_img:
            dish.img = received_img
            dish.save()
        
        dish.section = Section.objects.get_by_name_and_restaurant(new_section, new_restaurant)[0]
        dish.section.save()
        dish.save()

        return dish

class ReservationEditForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["name", "phone", "guests", "date", "time", "comment"]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Номер тел.'}),
            'date': forms.TextInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'placeholder': 'Комментарий'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "input-field"})
    
    def save(self, restaurant_name, **kwargs):
        reservation = super().save(**kwargs)

        reservation.restaurant = Restaurant.objects.get_by_name(restaurant_name)[0]
        reservation.save()

        new_name = self.cleaned_data['name']
        new_phone = self.cleaned_data['phone']
        new_guests = self.cleaned_data['guests']
        new_date = self.cleaned_data['date']
        new_time = self.cleaned_data['time']
        new_comment = self.cleaned_data['comment']
        

        if new_name != reservation.name:
            reservation.name = new_name
            reservation.save()
        if new_phone != reservation.phone:
            reservation.phone = new_phone
            reservation.save()
        if new_guests != reservation.guests:
            reservation.guests = new_guests
            reservation.save()
        if new_date != reservation.date:
            reservation.date = new_date
            reservation.save()
        if new_time != reservation.time:
            reservation.time = new_time
            reservation.save()
        if new_comment != reservation.comment: 
            reservation.comment = new_comment
            reservation.save()

        return reservation

class ReservationAddForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["name", "phone", "guests", "date", "time", "comment"]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Номер тел.'}),
            'date': forms.TextInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'cols': 80, 'rows': 20, 'placeholder': 'Комментарий'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({"class": "input-field"})

    def save(self, restaurant_name, **kwargs):
        reservation = Reservation.objects.create(
                restaurant = Restaurant.objects.get_by_name(restaurant_name)[0],
                name = self.cleaned_data['name'],
                phone = self.cleaned_data['phone'],
                guests = self.cleaned_data['guests'],
                date = self.cleaned_data['date'],
                time = self.cleaned_data['time'],
                comment = self.cleaned_data['comment'],
            )
        
        return reservation

class ReviewForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user: User = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Review
        fields = ['title', 'content', 'verdict']

    def save(self, restaurant):
        naive_datetime = datetime.now()
        aware_datetime = make_aware(naive_datetime)
        profile = Profile.objects.get(user=self.user)
        review = Review.objects.create(
            profile = profile, 
            title = self.cleaned_data['title'], 
            content = self.cleaned_data['content'], 
            restaurant = Restaurant.objects.get(name=restaurant),
            date = aware_datetime,
            verdict = self.cleaned_data['verdict'],
        )

        return review

class RestaurantEditForm(forms.ModelForm):
    
    class Meta:
        model = Restaurant
        fields = "__all__"
        widgets = {
            'img': forms.FileInput(attrs={'type': 'file'}),
        }
    
    def save(self, request, **kwargs):
        restaurant = super().save(**kwargs)

        received_img = self.cleaned_data.get('img')
        new_name = self.cleaned_data.get('name')
        new_phone = self.cleaned_data.get('phone')
        new_address = self.cleaned_data.get('address')
        new_content = self.cleaned_data['content']

        if new_name != restaurant.name:
            restaurant.name = new_name
            restaurant.save()
        if new_address != restaurant.address:
            restaurant.address = new_address
            restaurant.save()
        if new_content != restaurant.content:
            restaurant.content = new_content
            restaurant.save()
        if new_phone != restaurant.phone:
            restaurant.phone = new_phone
            restaurant.save()
        if received_img:
            restaurant.img = received_img
            restaurant.save()
        
        return restaurant

    

