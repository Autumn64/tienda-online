// Si hay un token de sesión entonces no permite volver a visualizar la pantalla de login.
if (window.tienda_session) window.location.href = "index.html";

function setSession(token){
    // Guarda el token en la sesión actual, y se pierde cuando el usuario cierra el navegador.
    window.tienda_session = token;
}

function setPersistentSession(token){
    // Guarda el token de manera persistente; se conserva hasta que éste expire.
    localStorage.setItem("tienda-session", token);
}

async function tryLogin(email, password, authCode){
    // Hace la petición a la API especificando el usuario y la contraseña introducida.
    request = {
        "email": email,
        "password": password
    }

    // Si se introdujo el código de verificación en dos pasos, se incluye en la petición.
    if (authCode) request.auth = authCode;

    try{
        const response = await fetch("http://localhost:5000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(request)
        });

        const result = await response.json();

        if (result.status !== "success") throw new Error(result.message);

        //if (result.code === 202) throw new Error(result.message);

        return result.data;
    }catch (error){
        addMessage($(".container"), "error", error);
    }
    
}

$("#loginForm").on("submit", async e => {
    e.preventDefault();

    $(".alert").remove();

    const email = $("#loginEmail").val();
    const password = $("#loginPassword").val();
    const rememberMe = $("#rememberMeCheck").is(":checked")

    const user = await tryLogin(email, password);
    if (!user) return;
    
    // Si se llegó a este punto es porque el login fue correcto y ya se cuenta con
    // el token de sesión.
    setSession(user.token);
    if (rememberMe) setPersistentSession(user.token);

    window.location.href = "index.html";
});