$(() =>{
    fetch("https://storeapi.autumn64.xyz/api/products")
    .then(r => r.json())
    .then(response =>{
        for (element of response.data){
            addProductCard($("#mainContainer"), `https://storeapi.autumn64.xyz${element.imagen}`, 
            element.nombre, `$${element.precio}`, `product.html?id=${element.id}`);
        }
    });
});