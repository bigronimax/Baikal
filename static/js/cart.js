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

const dish_buttons = document.getElementsByClassName("dish__plus")

for (let i = 0; i < dish_buttons.length; i++) {
    const dish = dish_buttons[i];
    dish.addEventListener('click', () => {

        const formData = new FormData();
        
        formData.append("dish_id", dish.dataset.id)

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
                document.getElementById("cart_quantity").textContent = data.qty
            });
    })
}
