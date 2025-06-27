from flask import Blueprint, send_file, request, redirect, url_for, flash
import os
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime

view_personal_print_bp = Blueprint('view_personal_print_bp', __name__)

@view_personal_print_bp.route('/print-personal/<path:filepath>', methods=['POST'])
def print_personal(filepath):
    try:
        selected_pages = request.form.getlist('selected_pages')
        if not selected_pages:
            flash("❌ Please select at least one page to print.", "danger")
            return redirect(url_for('view_personal_advanced_bp.advanced_tools_personal', filepath=filepath))

        full_path = os.path.join('Personal_Docs', filepath)
        if not os.path.exists(full_path):
            return "File not found", 404

        reader = PdfReader(full_path)
        writer = PdfWriter()

        for p in selected_pages:
            page_num = int(p) - 1  # 0-based
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        temp_dir = "uploads/print_temp"
        os.makedirs(temp_dir, exist_ok=True)
        output_path = os.path.join(temp_dir, f"print_pages_{timestamp}.pdf")

        with open(output_path, "wb") as f:
            writer.write(f)

        return send_file(output_path, as_attachment=False)

    except Exception as e:
        print("❌ Print Error:", e)
        flash("❌ Failed to print selected pages.", "danger")
        return redirect(url_for('view_personal_advanced_bp.advanced_tools_personal', filepath=filepath))
