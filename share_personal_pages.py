from flask import Blueprint, request, send_file, flash, redirect, url_for
import fitz  # PyMuPDF
import os
from datetime import datetime

share_personal_bp = Blueprint('share_personal_bp', __name__)

@share_personal_bp.route('/share-personal-pages/<path:filepath>', methods=['POST'])
def share_personal_pages(filepath):
    try:
        selected_pages = request.form.getlist('selected_pages')
        if not selected_pages:
            flash("❌ Please select at least one page to share.", "danger")
            return redirect(url_for('view_personal_advanced_bp.view_personal_advanced', filepath=filepath))

        page_numbers = [int(p) - 1 for p in selected_pages]
        filepath = filepath.replace("\\", "/")

        pdf = fitz.open(filepath)
        output = fitz.open()

        for i in page_numbers:
            if 0 <= i < len(pdf):
                output.insert_pdf(pdf, from_page=i, to_page=i)

        pdf.close()

        output_dir = "uploads/share_ready"
        os.makedirs(output_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"share_ready_personal_{timestamp}.pdf"
        output_path = os.path.join(output_dir, output_filename)

        output.save(output_path)
        output.close()

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("❌ Error in share_personal_pages:", e)
        flash("❌ Failed to prepare share file.", "danger")
        return redirect(url_for('view_personal_advanced_bp.view_personal_advanced', filepath=filepath))
