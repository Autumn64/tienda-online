if (localStorage.getItem("user")) window.location.href = "index.html";

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

        const result = await response.json()

        console.log(result)

        if (response.status != 200) throw new Error(result.message);

        addMessage($(".container"), "success", `Bienvenid@, ${result.data['username']}`);
        addMessage($(".container"), "info", `Eres usuario de tipo "${result.data['tipo']}"`);

    }catch (error){
        addMessage($(".container"), "error", error);
    }
    
}

$("#loginForm").on("submit", e => {
    e.preventDefault();

    $(".alert").remove();

    const email = $("#loginEmail").val();
    const password = $("#loginPassword").val();

    getUser(email, password);
});

/*$("#loginForm").on("submit", e => {
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
});*/