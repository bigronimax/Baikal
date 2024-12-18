from app.models import Dish, OrderDish, Restaurant
from django.db.models import Sum, F

class Cart():
    def __init__(self, request):
        self.session = request.session
        
        cart = self.session.get('session_key')
        d = dict.fromkeys(Restaurant.objects.all().values_list('name', flat=True))

        if 'session_key' not in request.session or self.session.get('session_key').keys() != d.keys():
            cart = self.session['session_key'] = d
            for i in cart.keys():
                cart[i] = {}

        self.cart = cart

    def add(self, dish, restaurant_name):
        dish_id = str(dish.id)

        if dish_id in self.cart[restaurant_name]:
            self.cart[restaurant_name][dish_id] = self.cart[restaurant_name][dish_id] + 1
        else:
            self.cart[restaurant_name][dish_id] = 1

        self.session.modified = True

        return self.cart[restaurant_name][dish_id]
    
    def delete(self, dish, restaurant_name):
        dish_id = str(dish.id)
        if dish_id in self.cart[restaurant_name]:
            if self.cart[restaurant_name][dish_id] > 1:
                self.cart[restaurant_name][dish_id] = self.cart[restaurant_name][dish_id] - 1
                self.session.modified = True
                return self.cart[restaurant_name][dish_id]
            else:
                del self.cart[restaurant_name][dish_id] 
                self.session.modified = True
                return 0
        return 0
    
    def __len__(self, restaurant_name):
        return sum(self.cart[restaurant_name].values())
    
    def get_dishes(self, restaurant_name):
        dishes_id = self.cart[restaurant_name].keys()
        order_dishes_id = []
        for index in dishes_id:
            dish = Dish.objects.get(id=index)
            orderDish = OrderDish.objects.create(
                dish = dish,
                quantity = self.cart[restaurant_name][index]
            )
            order_dishes_id.append(orderDish.id)
        orderDishes = OrderDish.objects.filter(id__in = order_dishes_id)
        return orderDishes
    
    def get_sum_cost(self, restaurant_name):
        dishes = self.get_dishes(restaurant_name=restaurant_name)
        return dishes.aggregate(total=Sum(F('dish__price') * F('quantity')))['total']
    
    def empty(self, restaurant_name):
        self.cart[restaurant_name].clear()
        self.session.modified = True