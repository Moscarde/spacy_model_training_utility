// Função para capturar o texto selecionado
function getSelectedText() {
    const selection = window.getSelection();
    return selection.toString();
}

// Função para enviar o texto selecionado e a cor ao backend
function sendSelectedText(color) {
    const selectedText = getSelectedText();
    if (selectedText) {
        fetch('/marcador', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: selectedText,
                color: color
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Texto destacado com sucesso:", selectedText);
                    console.log("Posições:", data.pos);
                    highlightText(selectedText, color);
                }
            })
            .catch(error => console.error('Erro ao enviar o texto:', error));
    } else {
        console.log("Nenhum texto foi selecionado.");
    }
}

// Função para destacar o texto no frontend
function highlightText(text, color) {
    const textContentElement = document.getElementById('text-content');
    const innerHTML = textContentElement.innerHTML;
    const regex = new RegExp(`(${text})`, 'gi');
    const highlightClass = `highlight-${color}`;
    textContentElement.innerHTML = innerHTML.replace(regex, `<span class="${highlightClass}">$1</span>`);
}

function removeAllHighlights() {
    fetch('/remover-maracacoes', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Todas as marcações removidas.');
                location.reload(); // Recarrega a página para remover as marcações
            }
        });
}
