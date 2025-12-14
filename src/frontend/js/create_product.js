$("#productForm").on("submit", e =>{
    e.preventDefault();

    /*
        Haciendo QA descubrimos que se podía presionar el botón varias veces,
        lo que lleva a duplicados. Entonces deshabilitamos el botón para que 
        ya no se pueda hacer eso.
    */
    $("#submitBtn").prop("disabled", true);

    const formData = new FormData($("#productForm").get(0));

    // Reemplaza los saltos de línea por <br>.
    const description = $("#productDescription").val();
    formData.set("productDescription", description.replace(/\r?\n/g, "<br>"));

    fetch("https://storeapi.autumn64.xyz/api/products/", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${sessionStorage.getItem("tienda-session")}`
        },
        body: formData
    })
    .then(r => r.json())
    .then(response => {
        if (response.status !== "success") throw new Error(response.message);

        Swal.fire({
            "title": "Producto agregado con éxito",
            "text": response.message,
            "icon": "success"
        })
        .then(result => window.location.href = "create_product.html");
    })
    .catch(error => {
        $("#submitBtn").prop("disabled", false);
        Swal.fire({
            "title": "Error al agregar producto",
            "text": error,
            "icon": "error"
        });
    });
});

$(() =>{
    if (!sessionStorage.getItem("tienda-session")) window.location.href = "index.html";

    if (!sessionStorage.getItem("tienda-usertype") || sessionStorage.getItem("tienda-usertype") !== "admin") {
        $("#forbidden").show("slow");
        return;
    }

    $("#productPanel").show("slow");
});