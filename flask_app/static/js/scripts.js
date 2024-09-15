// Função para capturar o texto selecionado
function getSelectedText() {
    const selection = window.getSelection();
    return selection.toString();
}

// Função para enviar o texto selecionado e a cor ao backend
function sendSelectedText(label) {
    const selectedText = getSelectedText();
    console.log("selectedText", selectedText)
    console.log("Label", label)
    if (selectedText) {
        fetch('/highlight', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: selectedText,
                label: label
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Texto destacado com sucesso:", selectedText);
                    console.log("Posições:", data.pos);
                    highlightText(selectedText, label);
                }
            })
            .catch(error => console.error('Erro ao enviar o texto:', error));
    } else {
        console.log("Nenhum texto foi selecionado.");
    }
}

// Função para destacar o texto no frontend
function highlightText(text, label) {
    const textContentElement = document.getElementById('text-content');
    const innerHTML = textContentElement.innerHTML;
    const regex = new RegExp(`(${text})`, 'gi');
    const highlightClass = `highlight-${label}`;
    textContentElement.innerHTML = innerHTML.replace(regex, `<span class="${highlightClass}">$1</span>`);
}

// Função para remover todas as marcações
function removeAllHighlights() {
    fetch('/remove-highlights', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Todas as marcações removidas.');
                location.reload(); // Recarrega a página para remover as marcações
            }
        });
}
