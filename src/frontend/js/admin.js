function showMessage(title, text, icon, callback){
    Swal.fire({
        "title": title,
        "text": text,
        "icon": icon
    })
    .then(callback ? callback : () => {});
}

function removeProduct(e){
    e.preventDefault();

    const id = $(this).attr("data-cart-id");

    Swal.fire({
        title: "¿Deseas eliminar este producto?",
        text: "Esta acción no se puede deshacer.",
        icon: "question",
        showCancelButton: true,
        confirmButtonText: "Sí",
        cancelButtonText: "No"
    })
    .then(result =>{
        if (!result.isConfirmed) return;

        fetch(`https://storeapi.autumn64.xyz/api/products/${id}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${sessionStorage.getItem("tienda-session")}`
            }
        })
        .then(r => r.json())
        .then(response =>{
            if (response.status !== "success") throw new Error(response.message);

            showMessage("Producto eliminado", response.message, "success", () =>  window.location.reload());
        })
        .catch(error => {
            showMessage("Error al eliminar producto", error, "error", null);
        });
    });
}

function showProducts(){
    fetch("https://storeapi.autumn64.xyz/api/products/")
    .then(r => r.json())
    .then(response =>{
        for (element of response.data){
            addAdminProduct(
                $("#productsContainer"),
                element.id,
                `https://storeapi.autumn64.xyz${element.imagen}`,
                element.nombre,
                true
            );
        }

        $(".rmCol button").on("click", removeProduct);
    });
}

$(() =>{
    if (!sessionStorage.getItem("tienda-session")) window.location.href = "index.html";

    if (!sessionStorage.getItem("tienda-usertype") || sessionStorage.getItem("tienda-usertype") !== "admin") {
        $("#forbidden").show("slow");
        return;
    }

    showProducts();

    $("#adminPanel").show("slow");
});