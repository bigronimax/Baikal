from app.models import Dish

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
            print(self.cart[dish_id])
            print(self.cart)
            self.cart[dish_id] = self.cart[dish_id] + 1
        else:
            self.cart[dish_id] = 1

        self.session.modified = True
    
    def __len__(self):
        return sum(self.cart.values())
    
    def get_dishes(self):
        dishes_id = self.cart.keys()
        dishes = Dish.objects.filter(id__in = dishes_id)
        for id in dishes_id:
            dish = Dish.objects.get(id=id)
            dish.quantity = self.cart[id]
            dish.save()
        return dishes