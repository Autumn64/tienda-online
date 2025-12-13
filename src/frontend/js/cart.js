const currentCart = localStorage.getItem("tienda-cart") ? JSON.parse(localStorage.getItem("tienda-cart")) : {};
let totalPrice = 0.0

function updateCart(product, qty){
    currentCart[product]["qty"] = qty;
    localStorage.setItem("tienda-cart", JSON.stringify(currentCart));
}

function setTotalPrice(){
    totalPrice = 0.0

    $(".totalProdPrice").each(function (){
        let precio = Number.parseFloat($(this).text());
        totalPrice += precio;
    });

    $("#totalPrice").text(`Precio total: $${totalPrice}`);
}

function changeProdQty(e){
    /*
        Si el usuario cambia la cantidad de producto a comprar, que se refleje
        tanto en el subtotal de ese producto como en el precio total.
    */
    e.preventDefault();
    const max = Number.parseInt($(this).attr("max"));
    const value = Number.parseInt($(this).val());
    if (value > max) $(this).val(max);

    const ogPrice = $(this).parent().parent().find(".uProdPrice").text();
    const $subtotal = $(this).parent().parent().find(".totalProdPrice");

    $subtotal.text(Number.parseFloat($(this).val()) * Number.parseFloat(ogPrice));

    setTotalPrice();
    updateCart($(this).attr("data-cart-id"), $(this).val());
}

function removeProduct(e){
    /*
        Lanza el mensaje de confirmación y, en caso de ser aceptado, elimina la clave
        de ese producto en específico del diccionario y actualiza el localStorage.
    */
    e.preventDefault();
    
    const id = $(this).attr("data-cart-id");

    Swal.fire({
        title: "Confirmar",
        text: "¿Deseas eliminar este producto del carrito?",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sí",
        cancelButtonText: "No"
    })
    .then(result =>{
        if (!result.isConfirmed) return;

        delete currentCart[id];
        localStorage.setItem("tienda-cart", JSON.stringify(currentCart));

        window.location.reload();
    });
}

async function addProduct(id, quantity){
    /*
        Hace la petición a la API para obtener la información de cada producto,
        y lo inserta en la página.
    */
    r = await fetch(`http://localhost:5000/api/products/${id}`);
    response = await r.json();
    addCartProduct(
        $("#cartContainer"), 
        id,
        `http://localhost:5000${response.data["imagenes"][0]}`,
        response.data["nombre"],
        response.data["stock"],
        quantity,
        response.data["precio"]
    );
}

function buyCart(e){
    e.preventDefault();

    fetch("http://localhost:5000/api/checkout", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem("tienda-session")}`
        },
        body: localStorage.getItem("tienda-cart")
    })
    .then(r => r.json())
    .then(response =>{
        if (response.status !== "success") throw new Error(response.message);

        window.location.href = response.data["url"];
    })
    .catch(error =>{
        Swal.fire({
            title: "Error al realizar la compra",
            text: error,
            icon: "error",
        });
    });
}

$("#backBtn").on("click", e =>{
    e.preventDefault();
    history.back();
});

templatesReady.then(async () =>{
    if(!sessionStorage.getItem("tienda-session")) window.location.href = "index.html";

    if (Object.keys(currentCart).length < 1){
        // Si no hay productos en el carrito, oculta la interfaz y muestra los mensajes correspondientes.
        $("#bodyContainer").hide("slow");
        addMessage($("#errorsContainer"), "error", "No hay productos en el carrito.")
        addMessage($("#errorsContainer"), "info", "Agrega productos al carrito para verlos aquí.")
        $("#errorsContainer").show("slow");
        return;
    }

    for(let key in currentCart){
        await addProduct(key, currentCart[key]["qty"]);
    }

    setTotalPrice();

    // Estos inputs son para la cantidad del producto.
    $(".qtyCol").find("input").on("change", changeProdQty);
    // Botones de eliminar producto.
    $(".rmCol").find(".btn").on("click", removeProduct);

    $("#purchaseBtn").on("click", buyCart);
});