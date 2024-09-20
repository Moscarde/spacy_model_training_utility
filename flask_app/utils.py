import os
import fitz  # PyMuPDF
import pdfplumber


def extract_text_from_pdf(pdf_file):
    pdf_bytes = pdf_file.read()
    # Abre o arquivo PDF a partir dos bytes
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    extracted_text = []

    # Itera sobre todas as páginas
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Carrega a página
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            if "lines" in block:
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"]
                extracted_text.append(block_text.strip())

    return "\n".join(extracted_text)


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