from flask import Blueprint, render_template, request, send_file, abort
import os
import urllib.parse

smartview_panel_bp = Blueprint('smartview_panel', __name__, url_prefix='/smartview')

UPLOAD_FOLDER = 'uploads'

def list_pdf_files():
    files = []
    for root, dirs, filenames in os.walk(UPLOAD_FOLDER):
        for filename in filenames:
            if filename.lower().endswith('.pdf'):
                full_path = os.path.join(root, filename)
                rel_path = os.path.relpath(full_path, UPLOAD_FOLDER)
                parts = rel_path.split(os.sep)
                if len(parts) >= 3:
                    files.append({
                        'owner': parts[0],
                        'property': parts[1],
                        'doc_type': parts[2],
                        'filename': filename,
                        'path': rel_path.replace("\\", "/")
                    })
    return files

@smartview_panel_bp.route('/')
def smartview_panel():
    query = request.args.get('q', '').lower()
    all_files = list_pdf_files()

    if query:
        files = [f for f in all_files if query in f"{f['owner']} {f['property']} {f['doc_type']} {f['filename']}".lower()]
    else:
        files = all_files

    file_info = {}
    for f in files:
        file_info[f['filename']] = {
            'owner': f['owner'],
            'property_type': f['property']
        }

    return render_template('smartview.html', files=files, file_info=file_info)

@smartview_panel_bp.route('/download/<path:filepath>')
def download_file(filepath):
    full_path = os.path.join(UPLOAD_FOLDER, filepath)
    return send_file(full_path, as_attachment=True) if os.path.exists(full_path) else abort(404)

@smartview_panel_bp.route('/view/<path:filepath>')
def view_file(filepath):
    decoded_path = urllib.parse.unquote(filepath)
    full_path = os.path.join(UPLOAD_FOLDER, decoded_path)
    return send_file(full_path) if os.path.exists(full_path) else abort(404)

@smartview_panel_bp.route('/print/<path:filepath>')
def print_file(filepath):
    decoded_path = urllib.parse.unquote(filepath)
    full_path = os.path.join(UPLOAD_FOLDER, decoded_path)
    if not os.path.exists(full_path):
        return f"<h3>❌ File not found for printing: {full_path}</h3>", 404
    return render_template('print_preview.html', filepath=decoded_path)

@smartview_panel_bp.route('/share/<path:filepath>')
def share_file(filepath):
    decoded_path = urllib.parse.unquote(filepath)
    return render_template('smartview_share.html', filepath=decoded_path)

@smartview_panel_bp.route('/advanced/<path:filepath>')
def advanced_preview(filepath):
    decoded_path = urllib.parse.unquote(filepath)
    full_path = os.path.join(UPLOAD_FOLDER, decoded_path)
    if not os.path.exists(full_path):
        return f"<h3>❌ File not found for advanced view: {full_path}</h3>", 404
    return render_template('smartview_advanced.html', filepath=decoded_path)
