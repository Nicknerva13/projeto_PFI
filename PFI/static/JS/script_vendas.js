const csrftoken = getCookie('csrftoken');
let usuario = null;
let carrinho = [];
const LIMITE_MAXIMO = 30.0;

// AUTOCOMPLETE USUÁRIO
let timeoutAuto = null;

function autoCompletar() {
    const texto = document.getElementById("matricula").value.trim();
    const box = document.getElementById("autoResultados");

    if (texto.length < 1) {
        box.style.display = "none";
        return;
    }

    clearTimeout(timeoutAuto);
    timeoutAuto = setTimeout(() => {
        const url = isNaN(texto)
            ? `/api/usuario/?nome=${texto}`
            : `/api/usuario/?matricula=${texto}`;

        fetch(url)
            .then(resp => resp.json())
            .then(data => {
                if (!Array.isArray(data) || data.length === 0) {
                    box.innerHTML = "<div style='padding:8px;color:#666'>Nenhum usuário encontrado</div>";
                    box.style.display = "block";
                    return;
                }

                let html = "";
                data.forEach(u => {
                    html += `
                        <div style="padding:8px; cursor:pointer; border-bottom:1px solid #eee"
                             onclick='selecionarUsuario(${JSON.stringify(u)})'>
                            <strong>${u.nome}</strong><br>Matrícula: ${u.matricula}
                        </div>`;
                });

                box.innerHTML = html;
                box.style.display = "block";
            })
            .catch(console.error);
    }, 300);
}

function selecionarUsuario(u) {
    usuario = u;
    document.getElementById("matricula").value = u.nome;
    document.getElementById("autoResultados").style.display = "none";

    const limiteRestante = LIMITE_MAXIMO - usuario.saldo_em_dividas;

    document.getElementById('dadosUsuario').innerHTML = `
        <strong>Nome:</strong> ${u.nome}<br>
        <strong>Matrícula:</strong> ${u.matricula}<br>
        <strong>Limite Restante:</strong> R$ ${limiteRestante.toFixed(2)}
    `;
}

// SELEÇÃO DE PRODUTOS
document.querySelectorAll('.produto').forEach(el => {
    el.addEventListener('click', () => el.classList.toggle('selected'));
});

function adicionarProduto() {
    if (!usuario) {
        alert('Selecione um usuário primeiro!');
        return;
    }

    const qtd = parseInt(document.getElementById('quantidade').value);
    const selected = document.querySelectorAll('.produto.selected');

    if (selected.length === 0) {
        alert('Selecione pelo menos um produto!');
        return;
    }

    selected.forEach(el => {
        const id = el.dataset.id;
        const nome = el.dataset.nome;
        const preco = parseFloat(el.dataset.preco);
        const estoque = parseInt(el.dataset.estoque);
        const foto = el.dataset.foto;

        const existente = carrinho.find(i => i.id == id);
        const totalDesejado = existente ? existente.quantidade + qtd : qtd;

        if (totalDesejado > estoque) {
            alert(
                `Estoque insuficiente!\n\nProduto: ${nome}\nEstoque: ${estoque}\nTentou vender: ${totalDesejado}`
            );
            el.classList.remove('selected');
            return;
        }

        if (existente) {
            existente.quantidade += qtd;
            existente.total = existente.quantidade * existente.preco;
        } else {
            carrinho.push({
                id,
                nome,
                preco,
                quantidade: qtd,
                total: preco * qtd,
                foto
            });
        }

        el.classList.remove('selected');
    });

    atualizarTabela();
}

function atualizarTabela() {
    const tbody = document.querySelector('#tabelaVendas tbody');
    tbody.innerHTML = '';

    let totalGeral = 0;

    carrinho.forEach(item => {
        totalGeral += item.total;

        tbody.innerHTML += `
        <tr>
            <td><img src="${item.foto}" width="50" height="50" style="object-fit:contain;"> ${item.nome}</td>
            <td>${item.quantidade}</td>
            <td>R$ ${item.preco.toFixed(2)}</td>
            <td>R$ ${item.total.toFixed(2)}</td>
        </tr>
        `;
    });

    document.getElementById('total').innerText = totalGeral.toFixed(2);
}

function finalizarVenda() {
    if (!usuario) {
        alert('Selecione um usuário!');
        return;
    }

    if (carrinho.length === 0) {
        alert('Adicione produtos!');
        return;
    }

    const metodo = document.getElementById('metodoPagamento').value;

    if (metodo === "fiado") {
        const totalCarrinho = carrinho.reduce((acc, i) => acc + i.total, 0);
        const limiteRestante = LIMITE_MAXIMO - (usuario.saldo_em_dividas || 0);

        if (totalCarrinho > limiteRestante) {
            alert(
                `Compra acima do limite!\n\n` +
                `Limite restante: R$ ${limiteRestante.toFixed(2)}\n` +
                `Total da compra: R$ ${totalCarrinho.toFixed(2)}`
            );
            return;
        }
    }

    fetch('/api/registrar_venda/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            matricula: usuario.matricula,
            produtos: carrinho.map(i => ({
                id: i.id,
                quantidade: i.quantidade
            })),
            metodo_pagamento: metodo
        })
    })
        .then(resp => resp.json())
        .then(data => {
            if (data.sucesso) {
                alert('Venda registrada com sucesso!');
                location.reload();
            } else {
                alert('Erro: ' + data.erro);
            }
        })
        .catch(console.error);
}

function getCookie(name) {
    let cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');

        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}