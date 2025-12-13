$("#productForm").on("submit", e =>{
    e.preventDefault();

    const formData = new FormData($("#productForm").get(0));

    // Reemplaza los saltos de línea por <br>.
    const description = $("#productDescription").val();
    formData.set("productDescription", description.replace(/\r?\n/g, "<br>"));

    fetch("http://localhost:5000/api/products/", {
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
        Swal.fire({
            "title": "Error al agregar producto",
            "text": error,
            "icon": "error"
        });
    })
});

$(() =>{
    if (!sessionStorage.getItem("tienda-session")) window.location.href = "index.html";

    if (!sessionStorage.getItem("tienda-usertype") || sessionStorage.getItem("tienda-usertype") !== "admin") {
        $("#forbidden").show("slow");
        return;
    }

    $("#productPanel").show("slow");
});