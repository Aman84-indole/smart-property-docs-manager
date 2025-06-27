from flask import Blueprint, render_template, request, send_file
import os
from pdf2image import convert_from_path

# ✅ Poppler path — Windows users ke liye required
POPPLER_PATH = r"C:\Users\DELL\Desktop\Release-23.11.0-0\poppler-23.11.0\Library\bin"
# ✅ Blueprint create
smartview_advanced_bp = Blueprint('smartview_advanced', __name__)

@smartview_advanced_bp.route('/smartview/advanced/<owner>/<property_type>/<doc_type>/<filename>')
def smartview_advanced(owner, property_type, doc_type, filename):
    # ✅ Original PDF path
    pdf_path = os.path.join("uploads", owner, property_type, doc_type, filename)
    file_wo_ext = os.path.splitext(filename)[0]

    # ✅ Folder where images are stored
    folder_name = f"{owner}__{property_type}__{doc_type}__{file_wo_ext}"
    preview_dir = os.path.join("static", "previews", folder_name)

    # ✅ Create preview folder if not exists
    if not os.path.exists(preview_dir):
        os.makedirs(preview_dir)

    # ✅ Convert PDF to images only if not already done
    if not os.listdir(preview_dir):
        try:
            images = convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
            for i, image in enumerate(images):
                image.save(os.path.join(preview_dir, f"page_{i+1}.png"))
        except Exception as e:
            return f"Error converting PDF: {e}"

    # ✅ Sorted image filenames for rendering
    image_files = sorted(os.listdir(preview_dir))
    image_paths = [f"/static/previews/{folder_name}/{img}" for img in image_files]

    # ✅ Debug print
    print("🖼️ Image paths to render:", image_paths)

    return render_template('smartview_advanced.html',
                           image_paths=image_paths,
                           owner=owner,
                           property_type=property_type,
                           doc_type=doc_type,
                           filename=filename,
                           folder_name=folder_name)
