from flask import Blueprint, render_template, request
import os
from pdf2image import convert_from_path
import uuid
import re  # ✅ For clean_filename

view_personal_advanced_bp = Blueprint('view_personal_advanced_bp', __name__)

# ✅ Corrected Poppler Path
POPPLER_PATH = r"C:\Users\DELL\Desktop\Release-23.11.0-0\poppler-23.11.0\Library\bin"

# ✅ Clean Filename Function
def clean_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "_", name)
    return name.replace(" ", "_")

@view_personal_advanced_bp.route('/advanced-personal/<path:filepath>')
def advanced_tools_personal(filepath):
    pdf_path = os.path.normpath(os.path.join("Personal_Docs", filepath))  # ✅ Corrected path line
    output_folder = os.path.join('static', 'temp_images', str(uuid.uuid4()))
    os.makedirs(output_folder, exist_ok=True)

    pages = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    image_paths = []
    for i, page in enumerate(pages):
        filename = clean_filename(f'page_{i+1}.png')
        image_file = os.path.join(output_folder, filename)
        page.save(image_file, 'PNG')
        # ✅ Corrected path (fixed extra /static/static issue + slashes)
        image_paths.append(image_file.replace('\\', '/').replace('static/', ''))

    return render_template('view_personal_advanced.html', filepath=filepath, image_paths=image_paths)
