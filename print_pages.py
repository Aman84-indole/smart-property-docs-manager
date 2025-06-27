from flask import request, send_file, Blueprint
from PyPDF2 import PdfReader, PdfWriter
import os
from io import BytesIO

print_pages_bp = Blueprint('print_pages', __name__)

@print_pages_bp.route('/print_pages', methods=['POST'])
def print_pages():
    selected = request.form.getlist("selected_pages")
    if not selected:
        return "⚠️ Malik, please select pages to print."

    owner = request.form.get("owner")
    property_type = request.form.get("property_type")
    doc_type = request.form.get("doc_type")
    filename = request.form.get("filename")

    pdf_path = os.path.join("uploads", owner, property_type, doc_type, filename)

    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in selected:
            writer.add_page(reader.pages[int(page) - 1])

        output = BytesIO()
        writer.write(output)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=False
        )

    except Exception as e:
        return f"❌ Malik, printing failed: {e}"
