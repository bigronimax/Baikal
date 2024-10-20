from django.shortcuts import render

DISHES = {
    "Комбо":
    [{
        "id": i,
        "name": f'dish {i}',
        "content": f'content {i}',
        "price": f'{i*10} Р',
        "weight": f'{i*5} Г'

    } for i in range(3)],
    "Закуски":
    [{
        "id": i,
        "name": f'dish {i}',
        "content": f'content {i}',
        "price": f'{i*10} Р',
        "weight": f'{i*5} Г'

    } for i in range(5)],
    "Супы":
    [{
        "id": i,
        "name": f'dish {i}',
        "content": f'content {i}',
        "price": f'{i*10} Р',
        "weight": f'{i*5} Г'

    } for i in range(10)],
}

REVIEWS = [
    {
        "id": i,
        "title": f'review {i}',
        "content": f'content {i}',
        "date": f'{i*10}.{i*10}.2024',
        "verdict": f'Изумительно!'

    } for i in range(10)
]

ORDERS = [
    {
        "id": i,
        "guests": i,
        "dishes": [
            DISHES["Комбо"][0],
            DISHES["Комбо"][1],
            DISHES["Закуски"][0],
            DISHES["Закуски"][1],
            DISHES["Супы"][0],
        ],
        "date": f'{i*10}.{i*10}.2024',
        "time": f'{i*10}:{i*10}'
    } for i in range(10)
]

WORKERS = {
    "Официанты":
    [{
        "id": i,
        "name": f'worker {i}',
        "salary": f'{i*10} Р',
        "img": 'img/alisson.jpeg'

    } for i in range(3)],
    "Повара":
    [{
        "id": i,
        "name": f'worker {i}',
        "salary": f'{i*10} Р',
        "img": 'img/alisson.jpeg'

    } for i in range(5)],
    "Менеджеры":
    [{
        "id": i,
        "name": f'worker {i}',
        "salary": f'{i*10} Р',
        "img": 'img/alisson.jpeg'

    } for i in range(10)],
}


def main(request):
    return render(request, "main.html")

def hunterIndex(request):
    return render(request, "hunter__index.html")

def hunterReservation(request):
    return render(request, "hunter__reservation.html")

def hunterMenu(request):
    return render(request, "hunter__menu.html", context={"dishes": DISHES})

def hunterReviews(request):
    return render(request, "hunter__reviews.html", context={"reviews": REVIEWS})

def profile(request):
    return render(request, "profile.html")

def access(request):
    return render(request, "access.html")

def hunterAdminMenu(request):
    return render(request, "hunter__admin-menu.html", context={"dishes": DISHES})

def hunterAdminOrders(request):
    return render(request, "hunter__admin-orders.html", context={"orders": ORDERS})

def hunterAdminReservations(request):
    return render(request, "hunter__admin-reservations.html")

def hunterAdminReviews(request):
    return render(request, "hunter__admin-reviews.html", context={"reviews": REVIEWS})

def hunterAdminStaff(request):
    return render(request, "hunter__admin-staff.html", context={"workers": WORKERS})

def hunterAdminSupplies(request):
    return render(request, "hunter__admin-supplies.html")

def hunterAdminProfit(request):
    return render(request, "hunter__admin-profit.html")