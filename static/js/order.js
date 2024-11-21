function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const dish_minus = document.getElementsByClassName("number-minus")
const dish_plus = document.getElementsByClassName("number-plus")
const dish_counters = document.getElementsByClassName("number")

for (let i = 0; i < dish_counters.length; i++) {
    const plus = dish_plus[i];
    const minus = dish_minus[i];
    plus.addEventListener('click', () => {

        const formData = new FormData();
        
        formData.append("dish_id", plus.dataset.id)

        const request = new Request('cart/add', {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        });
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                dish_counters[i].innerHTML = data.dish_qty
                document.getElementById("cart_quantity").textContent = data.qty
                document.getElementById("total").textContent = data.sum_cost
            });
    })
    minus.addEventListener('click', () => {

        const formData = new FormData();

        formData.append("dish_id", minus.dataset.id)

        const request = new Request('cart/delete', {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        });
        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                dish_counters[i].innerHTML = data.dish_qty
                document.getElementById("cart_quantity").textContent = data.qty
                document.getElementById("total").textContent = data.sum_cost
                if (data.dish_qty == 0) {
                    location.reload()
                }
            });

    })
}
