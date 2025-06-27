from flask import Blueprint, render_template, request, redirect, flash, send_file, url_for
import os
from datetime import datetime
import csv
import io
import re
from PyPDF2 import PdfReader
from log_manager import log_upload  # ✅ Required for Report Panel

upload_module = Blueprint('upload_module', __name__, url_prefix='/upload')  # ✅ FIXED

UPLOAD_BASE = 'uploads'

owners = ['Ramesh', 'Suresh', 'Kiran']
property_types = ['House', 'Farm', 'Plot']
doc_types = ['Registry', 'Map', 'Patta', 'Tax']

upload_logs = []

# ✅ Filename cleaner
def clean_filename(name):
    name = name.strip()
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', name)

@upload_module.route('/', methods=['GET', 'POST'])  # ✅ FIXED to root of /upload
def upload_page():
    global owners, property_types, doc_types, upload_logs

    selected_owner = request.args.get('select_owner')
    selected_property = request.args.get('select_property')
    selected_doc = request.args.get('select_doc')

    if request.method == 'POST':
        new_owner = request.form.get('new_owner')
        new_property = request.form.get('new_property')
        new_doc = request.form.get('new_doc')

        if new_owner and new_owner.strip() and new_owner not in owners:
            owners.append(new_owner)
            flash(f"Owner '{new_owner}' added successfully!", "success")
            return redirect(url_for('upload_module.upload_page', select_owner=new_owner))

        if new_property and new_property.strip() and new_property not in property_types:
            property_types.append(new_property)
            flash(f"Property type '{new_property}' added successfully!", "success")
            return redirect(url_for('upload_module.upload_page', select_property=new_property))

        if new_doc and new_doc.strip() and new_doc not in doc_types:
            doc_types.append(new_doc)
            flash(f"Document type '{new_doc}' added successfully!", "success")
            return redirect(url_for('upload_module.upload_page', select_doc=new_doc))

        owner = request.form.get('owner')
        property_type = request.form.get('property_type')
        doc_type = request.form.get('doc_type')
        files = request.files.getlist('files')

        for file in files:
            file_status = 'Skipped'

            if file.filename.strip() == "":
                continue

            if file.filename.lower().endswith('.pdf'):
                file.stream.seek(0, os.SEEK_END)
                size = file.stream.tell()
                file.stream.seek(0)

                if size > 5 * 1024 * 1024:
                    file_status = 'Too Large'
                else:
                    save_path = os.path.join(UPLOAD_BASE, owner, property_type, doc_type)
                    os.makedirs(save_path, exist_ok=True)

                    cleaned_name = clean_filename(file.filename)
                    file_path = os.path.join(save_path, cleaned_name)

                    if os.path.exists(file_path):
                        file_status = 'Duplicate'
                    else:
                        file.save(file_path)
                        try:
                            reader = PdfReader(file_path)
                            _ = len(reader.pages)
                            file_status = 'Uploaded'
                            log_upload('admin', file.filename, owner, property_type, doc_type)  # ✅ Report sync
                        except Exception as e:
                            os.remove(file_path)
                            file_status = f"Corrupt PDF - {e}"

            upload_logs.insert(0, {
                'file': file.filename,
                'owner': owner,
                'property': property_type,
                'doc': doc_type,
                'status': file_status,
                'time': datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            })

        flash("Files processed successfully!", "info")
        return redirect(url_for('upload_module.upload_page',
                                select_owner=owner,
                                select_property=property_type,
                                select_doc=doc_type))

    return render_template('upload.html',
                           owners=owners,
                           property_types=property_types,
                           doc_types=doc_types,
                           logs=upload_logs,
                           selected_owner=selected_owner,
                           selected_property=selected_property,
                           selected_doc=selected_doc)

@upload_module.route('/export-log')
def export_log():
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['File Name', 'Owner', 'Property', 'Doc Type', 'Status', 'Time'])
    for row in upload_logs:
        cw.writerow([row['file'], row['owner'], row['property'], row['doc'], row['status'], row['time']])

    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='upload_summary.csv')
