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
        $("#prodPrice").text(response.data["precio"]);
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
    })
    .catch(error =>{
        if (error.message === "No se encontró el producto seleccionado.")
            window.location.href = "index.html";

        addMessage($("header"), "error", error);
    });
});