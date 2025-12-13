let prodStock = 0;

const addProductToCart = () =>{
    /*
        Genera el carrito en formato JSON, agrega el ID del producto y su cantidad,
        y lo guarda en el localStorage, así un carrito se vería de este modo:
        {
            "1": {
                "id": "1",
                "qty": 5
            },
            "3": {
                "id": "3",
                "qty": 2
            }
        }
    */
    const parameters = new URLSearchParams(window.location.search);

    const productId = parameters.get("id");
    let currentQty = Number.parseInt($("#prodQuantity").val());
    let currentCart = localStorage.getItem("tienda-cart") ? 
    JSON.parse(localStorage.getItem("tienda-cart")) : {};

    if (currentQty > prodStock) currentQty = prodStock;

    currentCart[productId] = {
        "id": productId,
        "qty": currentQty
    }

    localStorage.setItem("tienda-cart", JSON.stringify(currentCart));

    Swal.fire({
        title: "Producto agregado al carrito.",
        icon: "success",
        showCancelButton: true,
        confirmButtonText: "Ver carrito",
        cancelButtonText: "OK"
    })
    .then(result => {
        if (result.isConfirmed)
            window.location.href = "cart.html";
    });
}

$("#prodQuantity").on("change", e =>{
    e.preventDefault();
    const max = Number.parseInt($("#prodQuantity").attr("max"));
    if (Number.parseInt($("#prodQuantity").val()) > max)
        $("#prodQuantity").val(max);
});

$("#addToCartBtn").on("click", e =>{
    e.preventDefault();
    
    if (!sessionStorage.getItem("tienda-session")){
        Swal.fire({
            title: "Autenticación requerida.",
            text: "Necesitas iniciar sesión para realizar esa acción.",
            icon: "warning"
        });
        return;
    }

    addProductToCart();
});

$(() =>{
    const parameters = new URLSearchParams(window.location.search);

    if(!parameters.has("id") || isNaN(parameters.get("id")))
        window.location.href = "index.html";

    // Cambia la URL del botón de login para que apunte a la página del producto actual.
    $("#loginBtn a").attr("href", `login.html?next=product.html${encodeURIComponent(window.location.search)}`);

    // Petición GET a la API con el id del producto.
    fetch(`http://localhost:5000/api/products/${parameters.get("id")}`)
    .then(r => r.json())
    .then(response =>{
        if (response.status !== "success")
            throw new Error(response.message);

        // Actualiza los valores de cada parte de la página.
        $("#prodName").text(response.data["nombre"]);
        $("#prodPrice").text(`$${response.data["precio"]}`);
        $("#prodStock").text("Cantidad en stock: " + response.data["stock"]);
        $("#prodDescription").html(response.data["descripcion"]);

        // Cambia la cantidad máxima que se puede seleccionar para que no se pase del stock.
        $("#prodQuantity").attr("max", response.data["stock"]);

        // Agrega las imagenes al carrusel.
        for (let i = 0; i < response.data["imagenes"].length; i++){
            addCarouselImg($(".carousel-inner"), (i === 0), 
            `http://localhost:5000${response.data["imagenes"][i]}`, 
            `http://localhost:5000${response.data["imagenes"][i]}`);
        }

        prodStock = response.data["stock"];
    })
    .catch(error =>{
        if (error.message === "No se encontró el producto seleccionado.")
            window.location.href = "index.html";

        addMessage($("header"), "error", error);
    });
});