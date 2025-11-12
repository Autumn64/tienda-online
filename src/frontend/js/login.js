if (localStorage.getItem("user")) window.location.href = "index.html";

/*
    Prueba para ver que el control de usuarios se esté haciendo adecuadamente.
    Esto deberá reimplementarse usando la API.
*/

$("#loginForm").on("submit", e => {
    e.preventDefault();

    $(".alert").remove();
    
    const email = $("#loginEmail").val();
    const password = $("#loginPass").val();

    
    if (!["autumn64@disroot.org", "karymecg@gmail.com"].includes(email)){
        addMessage($(".container"), "error", "Login incorrecto.");
        return;
    }

    if (email === "autumn64@disroot.org"){
        localStorage.setItem("user", "admin");    
    }else {
        localStorage.setItem("user", "client");
    }

    setTimeout(() => window.location.href = "index.html", 500);
});