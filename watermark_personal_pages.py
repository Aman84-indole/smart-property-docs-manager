from flask import Blueprint, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from reportlab.pdfgen import canvas
import os

watermark_personal_bp = Blueprint('watermark_personal_bp', __name__)

@watermark_personal_bp.route('/personal-watermark/<path:filepath>', methods=['GET', 'POST'])
def add_personal_watermark(filepath):
    if request.method == 'POST':
        watermark_text = request.form['watermark']
        selected_pages_raw = request.form.get('selected_pages', '')
        selected_pages = [int(p)-1 for p in selected_pages_raw.split(',') if p.strip().isdigit()]

        pdf_path = os.path.join('Personal_Docs', filepath)
        output = BytesIO()

        try:
            reader = PdfReader(pdf_path)
            writer = PdfWriter()

            for i, page in enumerate(reader.pages):
                if i in selected_pages:
                    width = float(page.mediabox.width)
                    height = float(page.mediabox.height)

                    packet = BytesIO()
                    can = canvas.Canvas(packet, pagesize=(width, height))
                    can.setFont("Helvetica", 40)
                    can.setFillColorRGB(0.6, 0.6, 0.6, alpha=0.3)
                    can.drawCentredString(width / 2, height / 2, watermark_text)
                    can.save()
                    packet.seek(0)

                    watermark_pdf = PdfReader(packet)
                    watermark_page = watermark_pdf.pages[0]
                    page.merge_page(watermark_page)

                    writer.add_page(page)  # ✅ Only add watermarked page
                # else: skip unselected pages

            if not writer.pages:
                return "❌ No pages selected."

            writer.write(output)
            output.seek(0)
            return send_file(output, as_attachment=True, download_name='watermarked_selected_pages.pdf', mimetype='application/pdf')

        except Exception as e:
            return f"❌ Error: {e}"
