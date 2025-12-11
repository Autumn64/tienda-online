$(() =>{
    fetch("http://localhost:5000/api/products")
    .then(r => r.json())
    .then(response =>{
        for (element of response.data){
            addProductCard($("#mainContainer"), `http://localhost:5000${element.imagen}`, 
            element.nombre, `$${element.precio}`, `product.html?id=${element.id}`);
        }
    });
});