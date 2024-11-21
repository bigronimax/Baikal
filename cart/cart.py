from app.models import Dish, OrderDish
from django.db.models import Sum, F

class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, dish):
        dish_id = str(dish.id)

        if dish_id in self.cart:
            self.cart[dish_id] = self.cart[dish_id] + 1
        else:
            self.cart[dish_id] = 1

        self.session.modified = True

        return self.cart[dish_id]
    
    def delete(self, dish):
        dish_id = str(dish.id)

        if dish_id in self.cart:
            if self.cart[dish_id] > 1:
                self.cart[dish_id] = self.cart[dish_id] - 1
                self.session.modified = True
                return self.cart[dish_id]
            else:
                del self.cart[dish_id] 
                self.session.modified = True
                return 0
        return 0
    
    def __len__(self):
        return sum(self.cart.values())
    
    def get_dishes(self):
        dishes_id = self.cart.keys()
        order_dishes_id = []
        for id in dishes_id:
            dish = Dish.objects.get(id=id)
            orderDish = OrderDish(
                dish = dish,
                quantity = self.cart[id]
            )
            orderDish.save()
            order_dishes_id.append(orderDish.id)
        orderDishes = OrderDish.objects.filter(id__in = order_dishes_id)
        return orderDishes
    
    def get_sum_cost(self):
        dishes = self.get_dishes()
        return dishes.aggregate(total=Sum(F('dish__price') * F('quantity')))['total']
    
    def empty(self):
        self.session['session_key'] = {}