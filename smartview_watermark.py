from flask import Blueprint, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color
import os
from io import BytesIO

smartview_watermark_bp = Blueprint('smartview_watermark_bp', __name__)

@smartview_watermark_bp.route('/apply_watermark', methods=['POST'])
def apply_watermark():
    selected = request.form.getlist("selected_pages")
    owner = request.form.get("owner")
    property_type = request.form.get("property_type")
    doc_type = request.form.get("doc_type")
    filename = request.form.get("filename")

    if not selected:
        return "Malik ⚠️ Please select at least one page."

    pdf_path = os.path.join("uploads", owner, property_type, doc_type, filename)

    try:
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        # Watermark content setup
        watermark_text = "SmartProperty Confidential"
        for page_num in selected:
            index = int(page_num) - 1
            page = reader.pages[index]

            # Create watermark PDF
            watermark_buffer = BytesIO()
            c = canvas.Canvas(watermark_buffer, pagesize=letter)
            c.setFont("Helvetica", 40)
            c.setFillColor(Color(0.6, 0.6, 0.6, alpha=0.3))  # Light gray
            c.saveState()
            c.translate(300, 400)
            c.rotate(45)
            c.drawCentredString(0, 0, watermark_text)
            c.restoreState()
            c.save()

            # Merge watermark with PDF page
            watermark_buffer.seek(0)
            watermark_pdf = PdfReader(watermark_buffer)
            page.merge_page(watermark_pdf.pages[0])
            writer.add_page(page)

        # Save final result
        output = BytesIO()
        writer.write(output)
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name=f"{filename.replace('.pdf', '')}_watermarked.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        return f"❌ Malik, watermark failed: {e}"

# ✅ Remember to register blueprint in smartproperty_app.py like:
# from smartview_watermark import smartview_watermark_bp
# app.register_blueprint(smartview_watermark_bp)
