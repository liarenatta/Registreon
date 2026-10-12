document.addEventListener('DOMContentLoaded', function () {
    const bairroSelect = document.getElementById('bairro');
    const ruaSelect = document.getElementById('endereco');

    if (!bairroSelect || !ruaSelect) {
        console.error('Campo Bairro ou Rua não encontrado.');
        return;
    }

    // Guarda as ruas cadastradas antes de atualizar o campo.
    const todasAsRuas = Array.from(ruaSelect.options).filter(
        rua => rua.dataset.bairroId
    );

    function atualizarRuas() {
        const bairroId = bairroSelect.value;

        // Limpa as opções antigas.
        ruaSelect.innerHTML = '';

        const opcaoInicial = document.createElement('option');
        opcaoInicial.value = '';
        opcaoInicial.textContent = bairroId
            ? 'Selecione uma rua'
            : 'Selecione primeiro um bairro';
        opcaoInicial.disabled = true;
        opcaoInicial.selected = true;
        ruaSelect.appendChild(opcaoInicial);

        let quantidade = 0;

        todasAsRuas.forEach(function (rua) {
            if (rua.dataset.bairroId === bairroId) {
                const opcao = document.createElement('option');
                opcao.value = rua.value;
                opcao.textContent = rua.textContent.trim();
                ruaSelect.appendChild(opcao);
                quantidade++;
            }
        });

        // Habilita o campo quando existe um bairro selecionado.
        ruaSelect.disabled = !bairroId;

        if (bairroId && quantidade === 0) {
            opcaoInicial.textContent =
                'Nenhuma rua cadastrada neste bairro';
        }

        console.log('Bairro selecionado:', bairroId);
        console.log('Ruas encontradas:', quantidade);
    }

    bairroSelect.addEventListener('change', atualizarRuas);
    atualizarRuas();
});