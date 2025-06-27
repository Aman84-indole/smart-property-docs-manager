from flask import Blueprint, render_template, request
import os

view_personal_bp = Blueprint('view_personal_bp', __name__)

@view_personal_bp.route('/view-personal')
def view_personal_panel():
    base_folder = 'Personal_Docs'  # ✅ Your personal doc folder
    query = request.args.get('q', '').lower()
    file_list = []

    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                rel_path = os.path.relpath(os.path.join(root, file), base_folder)
                parts = rel_path.replace("\\", "/").split('/')
                if len(parts) >= 3:
                    person = parts[0]
                    doc_type = parts[1]
                    name = parts[2]
                    if query in file.lower():
                        file_list.append({
                            'file': file,
                            'person': person,
                            'type': doc_type,
                            'name': name,
                            'path': rel_path
                        })

    return render_template('view_personal.html', files=file_list, query=query)
