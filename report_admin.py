from flask import Blueprint, render_template, request, send_file
from log_manager import get_all_logs  # ✅ Real log function
import csv
import io

report_admin_bp = Blueprint('report_admin_bp', __name__)

@report_admin_bp.route('/report')
def report_page():
    all_logs = get_all_logs()

    user_filter = request.args.get('user', '')
    owner_filter = request.args.get('owner', '')
    property_filter = request.args.get('property', '')
    doc_filter = request.args.get('doc', '')

    filtered_logs = all_logs
    if user_filter:
        filtered_logs = [log for log in filtered_logs if log['user'] == user_filter]
    if owner_filter:
        filtered_logs = [log for log in filtered_logs if log['owner'] == owner_filter]
    if property_filter:
        filtered_logs = [log for log in filtered_logs if log['property'] == property_filter]
    if doc_filter:
        filtered_logs = [log for log in filtered_logs if log['doc'] == doc_filter]

    users = sorted(list(set(log['user'] for log in all_logs)))
    owners = sorted(list(set(log['owner'] for log in all_logs)))
    properties = sorted(list(set(log['property'] for log in all_logs)))
    docs = sorted(list(set(log['doc'] for log in all_logs)))

    return render_template('report.html', logs=filtered_logs,
                           users=users, owners=owners, properties=properties, docs=docs)

@report_admin_bp.route('/export-report')
def export_report():
    logs = get_all_logs()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['User', 'File Name', 'Owner', 'Property', 'Document', 'Date'])
    for row in logs:
        cw.writerow([row['user'], row['file'], row['owner'], row['property'], row['doc'], row['date']])

    output = io.BytesIO()
    output.write(si.getvalue().encode('utf-8'))
    output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='report_admin_summary.csv')
