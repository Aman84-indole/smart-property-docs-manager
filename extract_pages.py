from flask import Blueprint, request, render_template, send_file
from PyPDF2 import PdfReader, PdfWriter
import os
from datetime import datetime

extract_pages_bp = Blueprint('extract_pages_bp', __name__)

@extract_pages_bp.route('/extract_pages', methods=['POST'])
def extract_pages():
    owner = request.form['owner']
    property_type = request.form['property_type']
    doc_type = request.form['doc_type']
    filename = request.form['filename']
    selected_pages = request.form.getlist('selected_pages')

    if not selected_pages:
        return "No pages selected for extraction.", 400

    # 📄 Input PDF path
    input_path = os.path.join('uploads', owner, property_type, doc_type, filename)
    reader = PdfReader(input_path)
    writer = PdfWriter()

    # ✅ Add selected pages (1-indexed to 0-indexed)
    for page in selected_pages:
        page_index = int(page) - 1
        if 0 <= page_index < len(reader.pages):
            writer.add_page(reader.pages[page_index])

    # 📁 Output file path
    extracted_dir = os.path.join('static', 'extracted')
    os.makedirs(extracted_dir, exist_ok=True)

    base_name = os.path.splitext(filename)[0]
    output_file = f"{base_name}_extracted_{datetime.now().strftime('%d%m%Y_%H%M%S')}.pdf"
    output_path = os.path.join(extracted_dir, output_file)

    # 💾 Save extracted PDF
    with open(output_path, "wb") as f:
        writer.write(f)

    # 📤 Return file to user for download
    return send_file(output_path, as_attachment=True)
