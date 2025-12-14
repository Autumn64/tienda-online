const darkThemeMq = window.matchMedia("(prefers-color-scheme: dark)");

document.addEventListener("DOMContentLoaded", setTheme);

darkThemeMq.addEventListener("change", e => {
    if (localStorage.getItem("tienda-darkmode") !== null) return;

    localStorage.setItem("tienda-darkmode", e.matches ? true : false);
    setTheme();
});

function setTheme() {
    const currentTheme = localStorage.getItem("tienda-darkmode") === "true" ? "dark" : "light";
    $("html").attr("data-bs-theme", currentTheme);
}

function changeTheme(e) {
    e.preventDefault();
    
    if (localStorage.getItem("tienda-darkmode") === "true") localStorage.setItem("tienda-darkmode", false);
    else localStorage.setItem("tienda-darkmode", true);
    
    setTheme();
}

$("#theme-toggle").on("click", changeTheme);