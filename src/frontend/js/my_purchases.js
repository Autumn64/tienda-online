function addPurchases(data){
    let purchase_number = 1;

    data.forEach(purchase =>{
        addPurchaseCard(
            $("#purchasesContainer"), 
            purchase_number, 
            purchase["monto"], 
            purchase["fecha_compra"],
            true
        );

        for (element of purchase["productos"]){
            addPurchaseProduct(
                $(".purchase").first(),
                `https://storeapi.autumn64.xyz${element["imagen"]}`,
                element["nombre"],
                element["precio"],
                element["cantidad"]
            );
        }

        purchase_number += 1;
    });
}

function getPurchases(){
    fetch("https://storeapi.autumn64.xyz/api/purchases/", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${sessionStorage.getItem("tienda-session")}`
        }
    })
    .then(r => r.json())
    .then(response =>{
        if (response.status !== "success") throw new Error(response.message);
        if (response.data.length < 1){
            $("#bodyContainer").hide("slow");
            addMessage($("#errorsContainer"), "error", "No hay compras para mostrar.")
            addMessage($("#errorsContainer"), "info", "Haz compras en nuestra tienda, y podrás verlas aquí.")
            $("#errorsContainer").show("slow");
            return;
        }

        addPurchases(response.data);
    })
    .catch(error =>{
        Swal.fire({
            title: "Error al mostrar tus compras",
            text: error,
            icon: "error",
        });
    });
}

templatesReady.then(async () =>{
    if(!sessionStorage.getItem("tienda-session")) window.location.href = "index.html";

    getPurchases();
});