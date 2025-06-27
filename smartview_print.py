from flask import Blueprint, send_file, abort
import os
import urllib.parse

smartview_print_bp = Blueprint('smartview_print', __name__)

@smartview_print_bp.route('/smartview/print/<path:file_path>')
def smartview_print(file_path):
    # ✅ Decode any %20, %2F etc. in file path
    decoded_path = urllib.parse.unquote(file_path)

    # ✅ Construct absolute file path
    full_path = os.path.join("uploads", decoded_path)

    # ✅ Check and return file
    if os.path.isfile(full_path):
        return send_file(full_path, mimetype='application/pdf', as_attachment=False)
    else:
        return abort(404, description=f"📄 Malik, file not found at path: {full_path}")
