const nextPage = "login.html";

// Si hay un token de sesión entonces no permite volver a visualizar la pantalla de signup.
if (sessionStorage.getItem("tienda-session")) window.location.href = nextPage;

function showMessage(title, text, icon, callback){
    Swal.fire({
        "title": title,
        "text": text,
        "icon": icon
    })
    .then(callback ? callback : () => {});
}

function trySignup(username, email, password){
    // Hace la petición a la API para crear un nuevo usuario.
    fetch("https://storeapi.autumn64.xyz/api/auth/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "username": username,
            "email": email,
            "password": password
        })
    })
    .then(r => r.json())
    .then(response =>{
        if (response.status !== "success") throw new Error(response.message);

        showMessage("Éxito en el registro", response.message, "success", () => window.location.href = "login.html");
    })
    .catch(error =>{
        $("#signupForm button").prop("disabled", false);
        $("#loginSpinner").fadeOut("slow");
        showMessage("Error en el registro", error, "error", null);
    });
}


$("#signupForm").on("submit", async e => {
    e.preventDefault();

    $("#signupForm button").prop("disabled", true);
    $(".alert").remove();

    const username = $("#signupUser").val();  
    const email = $("#signupEmail").val();
    const password = $("#signupPassword").val();
    const password2 = $("#signupPassword2").val();

    if (password !== password2){
        $("#signupForm button").prop("disabled", false);
        showMessage("Error en el registro", "Las contraseñas no coinciden", "error", null);
        return;
    }

    $("#loginSpinner").fadeIn("slow");

    trySignup(username, email, password);
});