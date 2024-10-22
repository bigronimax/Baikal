from django.core.management import BaseCommand
from random import randint
from faker import Faker
from datetime import datetime
from app.models import Review, Restaurant, Worker, Order, Dish, Profile, User, Section, Menu, Profession

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **kwargs):
        num = kwargs['ratio']

        restaurants_size = 2
        reviews_size = num*10
        profiles_size = num
        orders_size = num
        workers_size = num
        dishes_size = num*5


        restaurants = [
            Restaurant(
                name = "Hunter",
                address = "aa:bb:cc",
                phoneNumber = fake.phone_number(),
            ),
            Restaurant(
                name = "Butin",
                address = "aa:bb:cc",
                phoneNumber = fake.phone_number(),
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
                name = "Супы" 
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
                isEnable = randint(0, 1),
                section = sections.get(pk=randint(1, sections_count)),
            ) 
            d.save()
            dishes.append(d)
        
        dishes = Dish.objects
        dishes_count = dishes.count()


        profiles = [
            Profile(
                profile = User.objects.create_user(username=f'{fake.name()}_{i}')
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
                date = str(fake.date_between(datetime(2022,1,1), datetime(2023,12,31))),
                verdict = 1,
                restaurant = restaurants.get(pk=randint(1, restaurants_count))
            ) 
            r.save()
            #r.restaurant.add()
            reviews.append(r)
     
        reviews = Review.objects
        reviews_count = reviews.count()
     
        orders = []

        for i in range(orders_size):
            o = Order(
                guests = randint(1, 7),
                date = str(fake.date_between(datetime(2022,1,1), datetime(2023,12,31))),
                time = fake.time(pattern = '%H:%M'),
                restaurant = restaurants.get(pk=randint(1, restaurants_count))
            ) 
            o.save()
            o.dishes.add(dishes.get(pk=randint(1, dishes_count)))
            orders.append(o)
        
        orders = Order.objects
        orders_count = orders.count()

        workers = []

        for i in range(workers_size):
            w = Worker(
                name = fake.sentence(nb_words=1),
                profession = professions.get(pk=randint(1, professions_count)),
                salary = randint(50000, 100000),
                avatar = 'img/alisson.jpeg'
            )
            w.save()
            workers.append(w)
        workers = Worker.objects
        workers_count = workers.count()


        # answers = [
        #     Answer(
        #         question = questions.get(pk=randint(1, questions_count)),
        #         content = fake.text(),
        #         rating = randint(0, 100000),
        #         profile = profiles.get(pk=randint(1, profiles_count)),
        #         date = str(fake.date_between(datetime(2022,1,1), datetime(2023,12,31)))
        #     ) for i in range(answers_size)
        # ]
        # Answer.objects.bulk_create(answers)
        # answers = Answer.objects
        # answers_count = answers.count()

        # questionLikes = [
        #     QuestionLike(
        #         profile = profiles.get(pk=randint(1, profiles_count)),
        #         question = questions.get(pk=randint(1, questions_count)),
        #         like = randint(0, 1)
        #     ) for i in range(likes_size // 2)
        # ]

        # QuestionLike.objects.bulk_create(questionLikes)

        # answerLikes = [
        #     AnswerLike(
        #         profile = profiles.get(pk=randint(1, profiles_count)),
        #         answer = answers.get(pk=randint(1, answers_count)),
        #         like = randint(0, 1)
        #     ) for i in range(likes_size // 2)
        # ]

        # AnswerLike.objects.bulk_create(answerLikes)
        