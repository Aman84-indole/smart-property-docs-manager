from flask import Blueprint, render_template, request, flash, redirect, url_for

smartview_share_bp = Blueprint('smartview_share', __name__, url_prefix='/share')

@smartview_share_bp.route('/', methods=['GET', 'POST'])
def share_file():
    if request.method == 'POST':
        email = request.form.get('email')
        whatsapp = request.form.get('whatsapp')
        file_path = request.form.get('file_path')
        filename = request.form.get('filename')
        if not email and not whatsapp:
            flash('Please enter Email or WhatsApp number to share.', 'danger')
        else:
            flash('✅ Sharing logic executed successfully (placeholder).', 'success')
            return redirect(url_for('smartview_share.share_file', file=filename, path=file_path))
    filename = request.args.get('file')
    file_path = request.args.get('path')
    return render_template('smartview_share.html', filename=filename, file_path=file_path)
