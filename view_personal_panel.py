# === view_personal_panel.py ===
import os
from flask import Blueprint, render_template, request

personal_view_bp = Blueprint('personal_view_bp', __name__)

@personal_view_bp.route('/personalview/')
def personal_view():
    folder_path = 'Personal_Docs'
    files = []
    query = request.args.get('q', '').lower()

    if os.path.exists(folder_path):
        for root, dirs, filenames in os.walk(folder_path):
            for filename in filenames:
                if filename.endswith('.pdf'):
                    owner = os.path.relpath(root, folder_path).split(os.sep)[0]
                    if query in filename.lower() or query in owner.lower():
                        files.append({
                            'file': filename,
                            'person': owner,
                            'type': 'Personal',
                            'name': os.path.splitext(filename)[0],
                            'path': os.path.relpath(os.path.join(root, filename), folder_path).replace("\\", "/")
                        })

    return render_template('view_personal.html', files=files, query=query)
