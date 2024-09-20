// Função para capturar o texto selecionado
function getSelectedText() {
    const selection = window.getSelection();
    selectedText = selection.toString().trim();

    if (selectedText === "") {
        alert("Selecione um texto!");
        return false; // Nenhum texto foi selecionado
    }
    return selectedText;
}

// Função que verifica e retorna o número de ocorrências
function checkRepetitions(selectedText, label) {
    const originalDiv = document.getElementById('original-text');
    const fullText = originalDiv.innerText;

    if (!selectedText) {
        return;
    }

    // Conta quantas vezes o selectedText aparece no fullText
    const occurrences = fullText.split(selectedText).length - 1;

    if (occurrences > 1) {
        alert("Multiplas ocorrencias do texto selecionado. Por favor, clique na ocorrência desejada.");

        let updatedText = "";
        let lastIndex = 0;
        let count = 0;
        let searchIndex = 0;

        // Envolve cada ocorrência em um <span> clicável
        while ((lastIndex = fullText.indexOf(selectedText, searchIndex)) !== -1) {
            // Adiciona o texto antes da ocorrência
            updatedText += fullText.substring(searchIndex, lastIndex);

            // Adiciona o <span> em volta do texto selecionado com a função para enviar a ocorrência
            updatedText += `<span style="color:blue; cursor:pointer; text-decoration:underline; font-weight:bold" onclick="sendOccurrence(${count}, '${selectedText}', '${label}')">${selectedText}</span>`;

            // Avança o searchIndex para depois da ocorrência atual
            searchIndex = lastIndex + selectedText.length;

            count++;
        }

        // Adiciona o resto do texto que sobrou
        updatedText += fullText.substring(searchIndex);

        // Atualiza o conteúdo da div com o texto modificado
        originalDiv.innerHTML = updatedText;

        return occurrences; // Retorna o número de ocorrências encontradas
    } else {
        return occurrences; // Retorna o número de ocorrências encontradas
    }
}

// Função para enviar o texto selecionado e a cor ao backend
function sendSelectedText(label) {
    const selectedText = getSelectedText();
    const occurrences = checkRepetitions(selectedText, label); // Verifica se há mais de uma ocorrência

    if (occurrences === 1) {
        fetchHighlightedText(selectedText, label);
    } else {
        console.log("Nenhuma ocorrência encontrada.");
        return
    }
}

// Função que envia o texto destacado e o índice ao backend
function fetchHighlightedText(text, label, index = 0) {
    console.log("Texto selecionado:", text);
    console.log("Label:", label);
    if (text) {
        fetch('/highlight', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                label: label,
                index: index // Envia o índice, se houver
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log("Texto destacado com sucesso:", text);
                    console.log("Posições:", data.pos);
                    highlightText(text, label);
                    location.reload();
                }
            })
            .catch(error => console.error('Erro ao enviar o texto:', error));
    } else {
        console.log("Nenhum texto foi selecionado.");
    }
}

// Função para enviar uma ocorrência específica clicada
function sendOccurrence(occurrenceNumber, selectedText, label) {
    console.log(`Enviando a ocorrência número ${occurrenceNumber} do texto: ${selectedText}`);
    fetchHighlightedText(selectedText, label, occurrenceNumber);
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

// Função para remover a última as marcações
function removeLastHighlight() {
    fetch('/remove-last-highlight', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            location.reload(); // Recarrega a página para remover as marcações
        });
}

document.getElementById('pdfFile').addEventListener('change', function () {
    document.getElementById('pdfForm').submit();
});


