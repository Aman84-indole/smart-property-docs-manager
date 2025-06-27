from flask import Blueprint, render_template, request, send_file
import os
import json
from datetime import datetime

view_others_bp = Blueprint('view_others_bp', __name__)

UPLOAD_FOLDER = 'uploads/others'  # ✅ Correct folder path

@view_others_bp.route('/view_others', methods=['GET'])
def view_others():
    selected_category = request.args.get('category', 'Company Document')
    selected_name = request.args.get('name', '')

    documents = []
    names_set = set()

    # ✅ Ensure folder exists
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    for folder in os.listdir(UPLOAD_FOLDER):
        folder_path = os.path.join(UPLOAD_FOLDER, folder)
        if os.path.isdir(folder_path):
            metadata_path = os.path.join(folder_path, 'metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)

                doc_category = metadata.get('category', '')
                doc_name = metadata.get('name', '')

                # Collect names for dropdown based on selected category
                if doc_category == selected_category:
                    names_set.add(doc_name)

                # Filter files to show in table
                if doc_category == selected_category and (selected_name == '' or doc_name == selected_name):
                    for file in os.listdir(folder_path):
                        if file.endswith('.pdf'):
                            file_path = os.path.join(folder_path, file)
                            file_size = round(os.path.getsize(file_path) / 1024, 2)
                            upload_time = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%d-%m-%Y %I:%M %p')

                            documents.append({
                                'file_name': file,
                                'name': doc_name,
                                'category': doc_category,
                                'file_path': file_path.replace('\\', '/'),
                                'size': f"{file_size} KB",
                                'date': upload_time,
                                'status': '✔ Uploaded'
                            })

    names_list = sorted(list(names_set))

    return render_template('view_others.html',
                           documents=documents,
                           selected_category=selected_category,
                           selected_name=selected_name,
                           names=names_list)

@view_others_bp.route('/download_others/<path:filepath>')
def download_others(filepath):
    return send_file(filepath, as_attachment=True)
