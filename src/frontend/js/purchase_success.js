$(() =>{
    if (!sessionStorage.getItem("tienda-session")) window.location.href = "index.html";
    
    localStorage.removeItem("tienda-cart");
});