from flask import Blueprint, render_template, request

view_personal_share_bp = Blueprint('view_personal_share_bp', __name__)

@view_personal_share_bp.route('/share-personal/<path:filepath>', methods=['GET', 'POST'])
def share_tools(filepath):
    selected_pages = []
    if request.method == 'POST':
        selected_pages = request.form.getlist('selected_pages')

    return render_template('share_confirmation_personal.html', filepath=filepath, selected_pages=selected_pages)
