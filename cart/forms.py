from django import forms
from app.models import Order, Restaurant
from django.utils import timezone

class OrderForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ["table", "guests"]
        widgets = {
            'table': forms.TextInput(attrs={'type': 'text'}),
            'guests': forms.TextInput(attrs={'type': 'text'}),
        }
    
    def save(self, dishes, restaurant_name, **kwargs):
        user = super().save(**kwargs)

        profile = user.profile
        table = self.cleaned_data.get('table')
        guests = self.cleaned_data.get('guests')
        order = Order.objects.create(
            profile=profile,
            table = table,
            guests = guests, 
            date = timezone.now().date(),
            restaurant = Restaurant.objects.get_by_name(restaurant_name)[0]
        )
        order.dishes.set(dishes)
        order.save()
        
        return order