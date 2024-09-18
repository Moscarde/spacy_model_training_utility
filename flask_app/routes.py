import json
import os

from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from flask_app.utils import (
    check_folder,
    extract_text_from_pdf,
    find_pos,
    highlight_annotations,
)

main_routes = Blueprint("main_routes", __name__)

pdf_text = None
json_filename = None
labels = json.load(open("labels.json"))


@main_routes.route("/", methods=["GET", "POST"])
def index():
    global pdf_text, json_filename
    extracted_text = None
    highlighted_text = None

    if request.method == "POST":
        pdf_file = request.files.get("pdf_file")

        if pdf_file:
            original_filename = pdf_file.filename
            json_filename = os.path.join("train_data", f"{original_filename}.json")
            if not os.path.exists(json_filename):
                check_folder()
                extracted_text = extract_text_from_pdf(pdf_file)
                with open(json_filename, "w", encoding="utf-8") as f:
                    json.dump(
                        {"content": extracted_text, "annotation": []},
                        f,
                        ensure_ascii=False,
                        indent=4,
                    )

            return redirect(url_for("main_routes.docs", filename=original_filename))

    return render_template("index.html")


@main_routes.route("/docs/<filename>")
def docs(filename):
    global pdf_text, json_filename

    original_filename = filename
    json_filename = os.path.join("train_data", f"{original_filename}.json")

    if os.path.exists(json_filename):
        with open(json_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            raw_text = data.get("content", "")
            annotations = data.get("annotation", [])
            extracted_text = highlight_annotations(raw_text, annotations)
    else:
        extracted_text = "Documento não encontrado"
        highlighted_text = None

    pdf_text = extracted_text
    return render_template(
        "index.html",
        extracted_text=extracted_text,
        labels=labels,
    )


@main_routes.route("/remove-highlights", methods=["POST"])
def remove_highlights():
    global json_filename
    if json_filename:
        try:
            with open(json_filename, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            json_data["annotation"] = []

            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

            return jsonify({"success": True})
        except Exception as e:
            print(f"Erro ao remover marcações: {e}")
            return jsonify({"success": False}), 500
    return jsonify({"success": False}), 400


@main_routes.route("/remove-last-highlight", methods=["POST"])
def remove_last_highlight():
    global json_filename
    if json_filename:
        try:
            with open(json_filename, "r", encoding="utf-8") as f:
                json_data = json.load(f)

            json_data["annotation"].pop()

            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

            return jsonify({"success": True})
        except Exception as e:
            print(f"Erro ao remover marcações: {e}")
            return jsonify({"success": False}), 500
    return jsonify({"success": False}), 400


@main_routes.route("/highlight", methods=["POST"])
def highlight():
    global pdf_text, json_filename
    data = request.get_json()
    target_text = data.get("text")
    label = data.get("label")

    pos = find_pos(pdf_text, target_text)

    if target_text and label and pos:
        with open(json_filename, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        annotation = {
            "label": [label],
            "points": [{"start": pos["start"], "end": pos["end"], "text": target_text}],
        }

        if "annotation" not in json_data:
            json_data["annotation"] = []

        json_data["annotation"].append(annotation)

        with open(json_filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        return jsonify({"success": True, "pos": pos, "color": label})

    return jsonify({"success": False}), 400
