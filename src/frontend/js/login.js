if (sessionStorage.getItem("session")) window.location.href = "index.html";

function setSession(token){
    sessionStorage.setItem("session", token);
}

function setPersistentSession(token){
    localStorage.setItem("session", token);
}

async function getUser(email, password){
    try{
        const response = await fetch("http://localhost:5000/api/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "email": email,
                "password": password
            })
        });

        const result = await response.json();

        if (response.status != 200) throw new Error(result.message);

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
    const user = await getUser(email, password);

    if (!user) return;
    
    setSession(user.token);
    if (rememberMe) setPersistentSession(user.token);

    window.location.href = "index.html";
});