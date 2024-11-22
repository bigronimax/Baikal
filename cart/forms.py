from django import forms
from app.models import Order, Restaurant
from django.utils import timezone
from datetime import datetime
from django.utils.timezone import make_aware

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ["table", "guests"]
        widgets = {
            'table': forms.TextInput(attrs={'type': 'text'}),
            'guests': forms.TextInput(attrs={'type': 'text'}),
        }
    
    def save(self, restaurant_name, **kwargs):
        user = super().save(**kwargs)
        naive_datetime = datetime.now()
        aware_datetime = make_aware(naive_datetime)

        profile = user.profile
        table = self.cleaned_data.get('table')
        guests = self.cleaned_data.get('guests')
        order = Order.objects.create(
            profile=profile,
            table = table,
            guests = guests, 
            date = aware_datetime,
            restaurant = Restaurant.objects.get_by_name(restaurant_name)[0]
        )
        
        return order