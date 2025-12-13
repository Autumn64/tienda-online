const switchScreen = () =>{
    // Animación que alterna entre la pantalla inicial de carga y la información ya desplegada.
    // Esto se implementó debido al retraso provocado por la petición fetch.
    $("#loading-screen").fadeOut("slow", () =>{
        $("#main-container").fadeIn("slow");
    });
}

const setInterface = user =>{
    // Oculta el botón de login y agrega el menú del usuario.
    $("#loginBtn").hide();
    $("#accountDropdown").show();

    if (user.type !== "admin") return;

    // Si el usuario es administrador incluye la sección de administración de productos.
    $("#adminMode").show();
    
}

async function getSession(token){
    // Hace la petición hacia el endpoint de los tokens, únicamente para verificar si el usuario
    // inició sesión, en cuyo caso se adapta la interfaz de la página.

    // Si no hay token no tiene sentido hacer ninguna petición
    if (!token) return null;

    try{
        const response = await fetch("https://storeapi.autumn64.xyz/api/tokens/", {
            method: "GET",
            headers: {
                // El cliente debe enviar una cabecera de autorización con el formato
                // `Authorization: Bearer TOKEN`.
                "Authorization": `Bearer ${token}`
            }
        });

        const result = await response.json();

        if (result.status !== "success"){
            // Si el servidor responde negativamente ante el token, se elimina para que no
            // se esté enviando a cada momento, ya que el resultado siempre sería el mismo.
            sessionStorage.removeItem("tienda-session");
            localStorage.removeItem("tienda-session");
            return;
        }

        return result.data;

    }catch (error){
        addMessage($(".container"), "error", error);
    }
}

$("#logoutBtn").on("click", () =>{
    // Elimina toda la información de la sesión y redirecciona a la página principal.
    sessionStorage.removeItem("tienda-session")
    localStorage.removeItem("tienda-session");
    localStorage.removeItem("tienda-cart");
    delete window.isAdmin;
    window.location.href = "index.html";
});

$(async () =>{
    if (localStorage.getItem("tienda-session")){
        // Si hay un token guardado, lo incluye en la sesión actual.
       sessionStorage.setItem("tienda-session", localStorage.getItem("tienda-session"));
    }

    const user = await getSession(sessionStorage.getItem("tienda-session"));

    switchScreen();

    // Si no hay información del usuario no hace nada más.
    if (!user) return;

    // Si hay usuario, pero no está verificado, redirecciona a la pantalla de verificación.
    if (!user.verificado) window.location.href = "verify.html";

    sessionStorage.setItem("tienda-usertype", user.type);

    setInterface(user);
});