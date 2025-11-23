function gerarRelatorio() {
    const periodo = document.getElementById("periodo").value;
    window.location.href = `/gerar-relatorio/?periodo=${periodo}`;
}

function exportarRelatorio() {
    const periodo = document.getElementById("periodo").value;
    window.location.href = `/exportar-relatorio/?periodo=${periodo}`;
}
