from django.core.management import BaseCommand
from random import randint
from faker import Faker
from datetime import datetime, date
from app.models import Review, Restaurant, Worker, Order, Dish, Profile, User, Section, Menu, Profession, Supply, OrderDish, Revenue
from calendar import Calendar, monthrange
from django.contrib.auth.models import User, Group, Permission

c = Calendar()
fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['ratio']

        restaurants_size = 2
        reviews_size = num * 10
        profiles_size = num
        orders_size = num * 100
        workers_size = num 
        dishes_size = num * 5
        order_dishes_size = num * 1000
        supplies_size = num 

        dates = [x for x in c.itermonthdates(date.today().year, date.today().month) if x.month == date.today().month]

        restaurants = [
            Restaurant(
                name = "Hunter",
                address = "Проспект чего-то там, дом 50",
                phone = +79999999999,
                content = "В Сибирском отеле разместился аутентичный ресторан настоящего охотника. Здесь вы не останетесь без эмоций и наслаждения."
            ),
            Restaurant(
                name = "Butin",
                address = "Проспект чего-то там, дом 80",
                phone = +78888888888,
                content = "Здесь каждый может отдохнуть “без галстука”, побыть собой, хорошо и вкусно провести время"
            )
        ]

        Restaurant.objects.bulk_create(restaurants)
        restaurants = Restaurant.objects
        restaurants_count = restaurants.count()

        menu = [
            Menu(
                restaurant = restaurants.get(pk=1)
            ),
            Menu(
                restaurant = restaurants.get(pk=2)
            )
        ]

        Menu.objects.bulk_create(menu)
        menu_objects = Menu.objects
        menu_count = menu_objects.count()

        professions = [
            Profession(
                restaurant = restaurants.get(pk=1),
                name = "Официанты"
            ),
            Profession(
                restaurant = restaurants.get(pk=2),
                name = "Официанты"
            ),
            Profession(
                restaurant = restaurants.get(pk=1),
                name = "Повара"
            ),
            Profession(
                restaurant = restaurants.get(pk=2),
                name = "Повара"
            ),
            Profession(
                restaurant = restaurants.get(pk=1),
                name = "Менеджеры"
            ),
            Profession(
                restaurant = restaurants.get(pk=2),
                name = "Менеджеры"
            )
        ]

        Profession.objects.bulk_create(professions)
        professions = Profession.objects
        professions_count = professions.count()

        sections = []

        for i in ["Hunter", "Butin"]:
            s = Section(
                menu = menu_objects.get_restaurant(i)[0],
                name = "Комбо" 
            )
            s.save()
            sections.append(s)
            s1 = Section(
                menu = menu_objects.get_restaurant(i)[0],
                name = "Закуски" 
            )
            s1.save()
            sections.append(s1)
            s2 = Section(
                menu = menu_objects.get_restaurant(i)[0],
                name = "Горячее" 
            )
            s2.save()
            sections.append(s2)

        sections = Section.objects
        sections_count = sections.count()
        
        dishes = []

        for i in range(dishes_size):
            d = Dish(
                name = fake.sentence(nb_words=1),
                content = fake.text(max_nb_chars=20),
                price = randint(400, 800),
                weight = randint(250, 500),
                section = sections.get(pk=randint(1, sections_count)),
            ) 
            d.save()
            dishes.append(d)
        
        dishes = Dish.objects
        dishes_count = dishes.count()

        dishes_hunter = dishes.filter(section__menu__restaurant__name="Hunter")
        dishes_hunter_count = dishes_hunter.count()

        dishes_butin = dishes.filter(section__menu__restaurant__name="Butin")
        dishes_butin_count = dishes_hunter.count()

        orders = []
        
        for i in range(orders_size):
            o = Order(
                guests = randint(1, 7),
                date = dates[randint(0, monthrange(date.today().year, date.today().month)[1] - 1)],
                restaurant = restaurants.get(pk=randint(1, restaurants_count))
            ) 
            o.save()
            orders.append(o)
        
        orders = Order.objects
        orders_count = orders.count()

        orders_hunter = orders.filter(restaurant__name="Hunter")
        orders_hunter_count = orders_hunter.count()

        orders_butin = orders.filter(restaurant__name="Butin")
        orders_butin_count = orders_hunter.count()

        orderDishes = []

        for i in range(order_dishes_size//2):
            od = OrderDish(
                dish = dishes_hunter.order_by('?')[0],
                quantity = randint(1, 7),
                order = orders_hunter.order_by('?')[0]
            ) 
            od.save()
            orderDishes.append(od)
        for i in range(order_dishes_size//2):
            od = OrderDish(
                dish = dishes_butin.order_by('?')[0],
                quantity = randint(1, 7),
                order = orders_butin.order_by('?')[0],
            ) 
            od.save()
            orderDishes.append(od)

        orderDishes = OrderDish.objects
        orderDishes_count = orderDishes.count()  

        profiles = [
            Profile(
                user = User.objects.create_user(username=f'{fake.name()}_{i}')
            ) for i in range(profiles_size)
        ]

        Profile.objects.bulk_create(profiles)
        profiles = Profile.objects
        profiles_count = profiles.count()
        
        reviews = []
    
        for i in range(reviews_size):
            r = Review(
                title = fake.sentence(nb_words=3),
                content = fake.text(),
                profile = profiles.get(pk=randint(1, profiles_count)),
                date = dates[randint(0, monthrange(date.today().year, date.today().month)[1] - 1)],
                verdict = Review.RATING_CHOICES[randint(0, len(Review.RATING_CHOICES)-1)][1],
                restaurant = restaurants.get(pk=randint(1, restaurants_count))
            ) 
            r.save()
            reviews.append(r)
     
        reviews = Review.objects
        reviews_count = reviews.count()

        supplies = []
    
        for i in range(supplies_size):
            s = Supply(
                name = fake.word(),
                provider = fake.word(),
                restaurant = restaurants.get(pk=randint(1, restaurants_count)),
                price = randint(400, 800),
                weight = randint(5, 20)
            ) 
            s.save()
            supplies.append(s)
     
        supplies = Supply.objects
        supplies_count = supplies.count()

        workers = []

        for i in range(workers_size):
            p =  Profile(
                user = User.objects.create_user(username=f'{fake.name()}_{i}')
            )
            p.save()
            w = Worker(
                profile = p,
                profession = professions.get(pk=randint(1, professions_count)),
                salary = randint(50000, 100000),
            )
            w.save()
            workers.append(w)
        workers = Worker.objects
        workers_count = workers.count()

        revenues = []

        for d in dates:
            r = Revenue(
                date = d
            )
            revenues.append(r)

        Revenue.objects.bulk_create(revenues)
        revenues = Revenue.objects
        revenues_count = revenues.count()



        view_order_permission = Permission.objects.get(codename='view_order') 

        add_reservation_permission = Permission.objects.get(codename='add_reservation') 
        change_reservation_permission = Permission.objects.get(codename='change_reservation') 
        delete_reservation_permission = Permission.objects.get(codename='delete_reservation') 
        view_reservation_permission = Permission.objects.get(codename='view_reservation') 

        view_review_permission = Permission.objects.get(codename='view_review')

        add_dish_permission = Permission.objects.get(codename='add_dish') 
        change_dish_permission = Permission.objects.get(codename='change_dish') 
        delete_dish_permission = Permission.objects.get(codename='delete_dish') 
        view_dish_permission = Permission.objects.get(codename='view_dish') 

        add_supply_permission = Permission.objects.get(codename='add_supply') 
        change_supply_permission = Permission.objects.get(codename='change_supply') 
        delete_supply_permission = Permission.objects.get(codename='delete_supply') 
        view_supply_permission = Permission.objects.get(codename='view_supply') 

        view_revenue_permission = Permission.objects.get(codename='view_revenue')

        add_worker_permission = Permission.objects.get(codename='add_worker') 
        change_worker_permission = Permission.objects.get(codename='change_worker') 
        delete_worker_permission = Permission.objects.get(codename='delete_worker') 
        view_worker_permission = Permission.objects.get(codename='view_worker') 

        waiter_group = Group.objects.create(
            name="waiter"
        )

        waiter_group.permissions.add(
            view_order_permission,
            add_reservation_permission,
            change_reservation_permission,
            delete_reservation_permission,
            view_reservation_permission,
            view_review_permission
        )

        chef_group = Group.objects.create(
            name="chef"
        )

        chef_group.permissions.add(
            view_order_permission,
            add_dish_permission,
            change_dish_permission,
            delete_dish_permission,
            view_dish_permission,
            add_supply_permission,
            change_supply_permission,
            delete_supply_permission,
            view_supply_permission,
            view_review_permission
        )
        

        manager_group = Group.objects.create(
            name="manager"
        )
        
        manager_group.permissions.add(
            view_order_permission,
            add_dish_permission,
            change_dish_permission,
            delete_dish_permission,
            view_dish_permission,
            add_supply_permission,
            change_supply_permission,
            delete_supply_permission,
            view_supply_permission,
            view_review_permission,
            view_revenue_permission,
            add_worker_permission,
            change_worker_permission,
            delete_worker_permission,
            view_worker_permission
        )

        workers = Worker.objects.all()

        for worker in workers: 
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
            