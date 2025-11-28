const setInterface = user =>{
    $("#loginBtn").hide();
    $("#accountDropdown").show();

    if (user.username == "1"){
        $("#adminMode").show();
    }
}

async function getSession(token){
    if (!token) return null;

    try{
        const response = await fetch("http://localhost:5000/api/tokens", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "token": token,
            })
        });

        const result = await response.json();

        if (response.status != 200) {
            localStorage.removeItem("session");
            sessionStorage.removeItem("session");
            return;
        };

        return result.data;

    }catch (error){
        addMessage($(".container"), "error", error);
    }
}

$("#logoutBtn").on("click", () =>{
    if (sessionStorage.getItem("session")) sessionStorage.removeItem("session");
    window.location.href = "index.html";
});

$(async () =>{
    if (localStorage.getItem("session")){
        sessionStorage.setItem("session", localStorage.getItem("session"));
    }

    const user = await getSession(sessionStorage.getItem("session"));

    if (user) setInterface(user);
});