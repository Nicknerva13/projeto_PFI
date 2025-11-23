function toggleImagem(checkbox) {
    const imagemId = checkbox.dataset.id;
    const ativo = checkbox.checked;

    fetch(`/carrosel/ativar/${imagemId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ ativo: ativo })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error("Erro ao atualizar status:", data.error);
            checkbox.checked = !ativo;
        }
    })
    .catch(err => {
        console.error("Erro na requisição:", err);
        checkbox.checked = !ativo;
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
