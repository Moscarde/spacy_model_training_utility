import os

import pdfplumber


def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    if text.strip() == "":
        text = "Nenhum texto encontrado no PDF."
    return text


def highlight_annotations(text, annotations):
    annotations = sorted(
        annotations, key=lambda x: x["points"][0]["start"], reverse=True
    )
    for annotation in annotations:
        label = annotation["label"][0].lower()
        for point in annotation["points"]:
            start = point["start"]
            end = point["end"]
            highlighted_text = (
                f'<span class="highlight-{label}">{text[start:end]}</span>'
            )
            text = text[:start] + highlighted_text + text[end:]
    return text


def find_pos(full_text, target_text, occurrence_index=0):
    # Encontrar todas as ocorrências da target_text no full_text
    occurrences = []
    start_pos = 0
    
    while start_pos < len(full_text):
        start_pos = full_text.find(target_text, start_pos)
        if start_pos == -1:
            break
        end_pos = start_pos + len(target_text)
        occurrences.append({"start": start_pos, "end": end_pos})
        start_pos = end_pos  # Atualiza para a próxima busca
    
    # Retorna a ocorrência específica baseada no índice
    if occurrence_index < len(occurrences):
        return occurrences[occurrence_index]
    
    return None  # Se não houver a ocorrência solicitada


def check_folder():
    if not os.path.exists("train_data"):
        os.makedirs("train_data")