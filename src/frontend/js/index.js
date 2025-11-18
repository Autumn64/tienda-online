// Evidentemente esto debe reimplementarse usando la API.
templatesReady.then(() =>{
    for (let i = 1; i < 6; i++){
        addProductCard($("#mainContainer"), `res/${i}.jpg`, `Producto ${i}`, `$${i * 176.5}`, "product.html");
    }

    for (let i = 1; i < 6; i++){
        addProductCard($("#mainContainer"), `res/${i}.jpg`, `Producto ${i+5}`, `$${i+5 * 76.2}`, "product.html");
    }
});