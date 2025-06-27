from flask import Blueprint, request, send_file, flash, redirect, url_for
import fitz  # PyMuPDF
import os
from datetime import datetime

extract_personal_bp = Blueprint('extract_personal_bp', __name__)

@extract_personal_bp.route('/extract-personal-pages/<path:filepath>', methods=['POST'])
def extract_personal_pages(filepath):
    try:
        selected_pages = request.form.getlist('selected_pages')
        if not selected_pages:
            flash("❌ Please select at least one page to extract.", "danger")
            return redirect(url_for('view_personal_advanced_bp.advanced_tools_personal', filepath=filepath))

        page_numbers = [int(p) - 1 for p in selected_pages]  # 0-based index
        filepath = filepath.replace("\\", "/")

        # ✅ Required fix: convert relative path to full path inside Personal_Docs
        pdf_path = os.path.normpath(os.path.join("Personal_Docs", filepath))

        pdf = fitz.open(pdf_path)
        output = fitz.open()

        for i in page_numbers:
            if 0 <= i < len(pdf):
                output.insert_pdf(pdf, from_page=i, to_page=i)

        pdf.close()

        output_dir = "uploads/extracted_files"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"extracted_personal_pages_{timestamp}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        output.save(output_path)
        output.close()

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("❌ Error in extract_personal_pages:", e)
        flash("❌ Failed to extract pages.", "danger")
        return redirect(url_for('view_personal_advanced_bp.advanced_tools_personal', filepath=filepath))
