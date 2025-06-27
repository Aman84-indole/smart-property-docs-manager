from flask import Blueprint, send_from_directory, abort
import os

personal_action_bp = Blueprint('personal_action_bp', __name__)

BASE_DIR = os.path.join(os.getcwd(), 'Personal_Docs')

# 🔹 Download Route
@personal_action_bp.route('/download-personal/<path:filepath>')
def download_personal(filepath):
    abs_path = os.path.join(BASE_DIR, filepath)
    if os.path.exists(abs_path):
        dir_name = os.path.dirname(abs_path)
        file_name = os.path.basename(abs_path)
        return send_from_directory(directory=dir_name, path=file_name, as_attachment=True)
    else:
        return abort(404)

# 🔹 View Route
@personal_action_bp.route('/view-personal/<path:filepath>')
def view_personal_file(filepath):
    abs_path = os.path.join(BASE_DIR, filepath)
    if os.path.exists(abs_path):
        dir_name = os.path.dirname(abs_path)
        file_name = os.path.basename(abs_path)
        return send_from_directory(directory=dir_name, path=file_name)
    else:
        return abort(404)

# 🔹 Print Route (same as view for now)
@personal_action_bp.route('/print-personal/<path:filepath>')
def print_personal(filepath):
    return view_personal_file(filepath)

# 🔹 Share Route (placeholder)
@personal_action_bp.route('/share-personal/<path:filepath>')
def share_personal(filepath):
    return f"📤 Share route accessed: {filepath}"

# 🔹 Advanced Route (placeholder)
@personal_action_bp.route('/advanced-personal/<path:filepath>')
def advanced_personal(filepath):
    return f"⚙️ Advanced tools for: {filepath}"
