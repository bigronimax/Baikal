from django import forms
from django.contrib.auth.models import User
from django.forms import ImageField, ValidationError
from django.core.validators import validate_email
from app.models import Review, Profile, Reservation


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
        Profile.objects.create(profile=user)
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
        received_date = self.cleaned_data.get('date')
        new_username = self.cleaned_data.get('username')
        new_email = self.cleaned_data.get('email')

        if new_username != user.username:
            user.username = new_username
        if new_email != user.email:
            user.email = new_email
        if received_avatar:
            profile.avatar = self.cleaned_data.get('avatar')
            profile.save()
        if received_date:
            profile.date = self.cleaned_data.get('date')
            profile.save()

        return user

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = "__all__"
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
    
    def save(self):
        reservation = Reservation(
            name = self.cleaned_data['name'],
            phone = self.cleaned_data['phone'],
            guests = self.cleaned_data['guests'],
            date = self.cleaned_data['date'],
            time = self.cleaned_data['time'],
            comment = self.cleaned_data['comment'],
        )
        reservation.save()

        return reservation

    

class ReviewForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.user: User = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Review
        fields = ['title', 'content']

    def save(self):
        profile = Profile.objects.get(profile=self.user)
        review = Review(profile=profile, title=self.cleaned_data['title'], content=self.cleaned_data['content'])
        review.save()

        return review
    
    

