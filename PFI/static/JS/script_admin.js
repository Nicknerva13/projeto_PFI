function toggleMenu() {
    const menu = document.getElementById("menu");
    const conteudo = document.getElementById("conteudo");

    menu.classList.toggle("show");

    // Se o menu abriu → ativa o blur
    if (menu.classList.contains("show")) {
        conteudo.classList.add("blurred");
    } else {
        conteudo.classList.remove("blurred");
    }
}
