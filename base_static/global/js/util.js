
// Ouvinte de eventos para verificar quando o campo de entrada muda
document.getElementById("pesquisaInput").addEventListener("input", function() {
    toogleBotaoLimparPesquisa();
});

// Ouvinte de eventos para o botão de limpar pesquisa
document.getElementById("limparPesquisaBtn").addEventListener("click", function() {    
    document.getElementById("pesquisaInput").value = "";
    document.getElementById("limparPesquisaBtn").style.display = "none";
});

// Função que verifica se o campo de pesquisa contém um valor inicial
function toogleBotaoLimparPesquisa() {
    let pesquisaInput = document.getElementById("pesquisaInput");
    let limparPesquisaBtn = document.getElementById("limparPesquisaBtn");

    // Verifica se há algum valor no campo de pesquisa
    if (pesquisaInput?.value.length > 0) {
        limparPesquisaBtn.style.display = "inline-block";
    } else {
        limparPesquisaBtn.style.display = "none";
    }
}

// Ouvinte de eventos para o evento DOMContentLoaded
document.addEventListener("DOMContentLoaded", function() {
    toogleBotaoLimparPesquisa();
});