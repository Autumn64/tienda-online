// Debe reimplementarse usando la API
if (localStorage.getItem("user")){
    $("#loginBtn").hide();
    $("#accountDropdown").show();
}

if (localStorage.getItem("user") === "admin"){
    $("#adminMode").show();
}

$("#logoutBtn").on("click", () =>{
    if (localStorage.getItem("user")) localStorage.removeItem("user");
    window.location.href = "index.html";
});