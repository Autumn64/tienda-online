$(() =>{
    if (!sessionStorage.getItem("tienda-session")) window.location.href = "index.html";

    if (!sessionStorage.getItem("tienda-usertype") || sessionStorage.getItem("tienda-usertype") !== "admin") {
        $("#forbidden").show("slow");
        return;
    }

    $("#adminPanel").show("slow");
});