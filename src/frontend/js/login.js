// Obtiene los parámetros de login de la URL para sacar la página a la que debe
// continuar después del login.
const parameters = new URLSearchParams(window.location.search);
const nextPage = parameters.has("next") ? parameters.get("next") : "index.html";

// Si hay un token de sesión entonces no permite volver a visualizar la pantalla de login.
if (sessionStorage.getItem("tienda-session")) window.location.href = nextPage;

function setSession(token){
    // Guarda el token en la sesión actual, y se pierde cuando el usuario cierra el navegador.
    sessionStorage.setItem("tienda-session", token)
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
        const response = await fetch("https://storeapi.autumn64.xyz/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(request)
        });

        const result = await response.json();

        if (result.status !== "success") throw new Error(result.message);

        // Retorna el resultado para comprobar que sí hubo respuesta, y para obtener
        // el mensaje que se mostrará al usuario.
        if (result.code === 202) return result;

        return result.data;
    }catch (error){
        $("#loginSpinner").fadeOut("slow", () =>{
            addMessage($(".container"), "error", error);
        }); 
    }
    
}

async function tfaVerification(message, email, password){
    // Genera mensaje con SweetAlert2
    code = await Swal.fire({
        title: "Verificación en dos pasos",
        text: message,
        icon: "warning",
        input: 'text',
        inputPlaceholder: "000000",
        showCancelButton: true,
    });

    if (!code.isConfirmed) return null;
    if(!code.value || code.value.trim() === "") return null;

    // Vuelve a intentar el inicio de sesión, esta vez con el código.
    return await tryLogin(email, password, code.value);
}

$("#loginForm").on("submit", async e => {
    e.preventDefault();

    $("#loginForm button").prop("disabled", true);
    $(".alert").remove();
    $("#loginSpinner").fadeIn("slow");

    const email = $("#loginEmail").val();
    const password = $("#loginPassword").val();
    const rememberMe = $("#rememberMeCheck").is(":checked")

    const response = await tryLogin(email, password);

    $("#loginForm button").prop("disabled", false);

    // Si no hubo respuesta es porque el login fue incorrecto.
    if (!response) return;

    // Se vuelve a hacer la petición, ahora solicitando el código de verificación.
    const user = await tfaVerification(response.message, email, password);

    if (!user){
        $("#loginSpinner").fadeOut("slow"); 
        return;
    };

    // Si se llegó a este punto es porque el login fue correcto y ya se cuenta con
    // el token de sesión.
    setSession(user.token);
    if (rememberMe) setPersistentSession(user.token);

    window.location.href = nextPage;
});