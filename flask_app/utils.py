import PyPDF2

def extract_text_from_pdf(pdf_file):
    text = ""
    reader = PyPDF2.PdfReader(pdf_file)
    for page in reader.pages:
        text += page.extract_text()
    return text

def highlight_annotations(text, annotations):
    annotations = sorted(annotations, key=lambda x: x["points"][0]["start"], reverse=True)
    for annotation in annotations:
        label = annotation["label"][0].lower()
        for point in annotation["points"]:
            start = point["start"]
            end = point["end"]
            highlighted_text = f'<span class="highlight-{label}">{text[start:end]}</span>'
            text = text[:start] + highlighted_text + text[end:]
    return text

def find_pos(full_text, target_text):
    start_pos = full_text.find(target_text)
    if start_pos != -1:
        end_pos = start_pos + len(target_text)
        return {"start": start_pos, "end": end_pos}
    return None