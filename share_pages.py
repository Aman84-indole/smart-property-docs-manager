from flask import Blueprint, request, render_template, send_file, redirect, url_for, flash
from PyPDF2 import PdfReader, PdfWriter
import os
from datetime import datetime

share_pages_bp = Blueprint('share_pages', __name__)

@share_pages_bp.route('/share_pages', methods=['POST'])
def share_pages():
    owner = request.form.get("owner")
    property_type = request.form.get("property_type")
    doc_type = request.form.get("doc_type")
    filename = request.form.get("filename")
    selected_pages = request.form.getlist("selected_pages")

    pdf_path = os.path.join("uploads", owner, property_type, doc_type, filename)
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    for page_num in selected_pages:
        idx = int(page_num) - 1
        if 0 <= idx < len(reader.pages):
            writer.add_page(reader.pages[idx])

    timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
    output_filename = f"{filename.split('.')[0]}_shared_{timestamp}.pdf"
    output_dir = os.path.join("static", "shared")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    with open(output_path, "wb") as f:
        writer.write(f)

    flash("PDF ready for sharing!", "success")

    # ✅ Return to a new Share UI with WhatsApp/Email buttons
    return render_template("share_options.html", filepath=f"shared/{output_filename}")
