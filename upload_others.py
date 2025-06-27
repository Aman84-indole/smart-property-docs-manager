# === upload_other.py ===
from flask import Blueprint, render_template, request, jsonify
import os, csv
from werkzeug.utils import secure_filename
from datetime import datetime

upload_other_bp = Blueprint('upload_other_bp', __name__)

UPLOAD_FOLDER = 'Personal_Docs'
DROPDOWN_FOLDER = 'dropdowns'
ALLOWED_EXTENSIONS = {'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DROPDOWN_FOLDER, exist_ok=True)

CSV_FILES = {
    'person_name': 'person_names.csv',
    'document_type': 'document_types.csv',
    'document_name': 'document_names.csv'
}

# Load values from CSV
def load_values(csv_file):
    path = os.path.join(DROPDOWN_FOLDER, csv_file)
    if not os.path.exists(path): return []
    with open(path, newline='', encoding='utf-8') as f:
        return sorted(set([row[0] for row in csv.reader(f) if row]))

# Save value to CSV
def save_value(field, value):
    filename = CSV_FILES.get(field)
    if not filename: return False
    path = os.path.join(DROPDOWN_FOLDER, filename)

    # Create the file if it doesn't exist
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            pass

    # Load existing values
    existing = load_values(filename)
    if value.strip() not in existing:
        with open(path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([value.strip()])
        print("✅ Saved to CSV:", path, "→", value)  # (Optional: for debug)
        return True
    return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_other_bp.route('/upload-other', methods=['GET', 'POST'])
def upload_other():
    logs = []
    if request.method == 'POST':
        person = request.form.get('person_name', '').strip()
        doctype = request.form.get('document_type', '').strip()
        docname = request.form.get('document_name', '').strip()
        files = request.files.getlist('pdf_files')

        if person and doctype and docname:
            save_dir = os.path.join(UPLOAD_FOLDER, person, doctype, docname)
            os.makedirs(save_dir, exist_ok=True)
            for file in files:
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(save_dir, filename)
                    if os.path.exists(filepath):
                        logs.append({'file': filename, 'owner': person, 'doctype': doctype, 'docname': docname, 'status': 'Duplicate', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')})
                    else:
                        file.save(filepath)
                        logs.append({'file': filename, 'owner': person, 'doctype': doctype, 'docname': docname, 'status': 'Uploaded', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')})
                else:
                    logs.append({'file': file.filename if file else 'None', 'owner': person, 'doctype': doctype, 'docname': docname, 'status': 'Error', 'time': datetime.now().strftime('%Y-%m-%d %H:%M')})

    dropdowns = {k: load_values(v) for k, v in CSV_FILES.items()}
    return render_template('upload_other.html', dropdowns=dropdowns, logs=logs)

@upload_other_bp.route('/add-dropdown-value', methods=['POST'])
def add_dropdown_value():
    field = request.form.get('field')
    value = request.form.get('value')
    success = save_value(field, value)
    return jsonify({'success': success, 'value': value})
