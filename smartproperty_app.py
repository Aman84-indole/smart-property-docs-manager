from flask import Flask, render_template
from upload_module import upload_module  # ✅ Upload module ka blueprint
from print_pages import print_pages_bp
from smartview_share import smartview_share_bp
from smartview_panel import smartview_panel_bp
from smartview_advanced import smartview_advanced_bp
from extract_pages import extract_pages_bp
from share_pages import share_pages_bp
from smartview_watermark import smartview_watermark_bp
from report_admin import report_admin_bp
from upload_others import upload_other_bp
from view_others import view_others_bp
from view_personal_print import view_personal_print_bp
from view_personal_share import view_personal_share_bp
from view_personal_advanced import view_personal_advanced_bp
from view_personal_panel import personal_view_bp
from personal_routes import personal_action_bp
from view_personal import view_personal_bp
from extract_personal_pages import extract_personal_bp
from print_personal_pages import print_personal_bp
from share_personal_pages import share_personal_bp
from watermark_personal_pages import watermark_personal_bp
from login import login_bp  # ✅ login_bp import karo
app = Flask(__name__)
app.secret_key = 'smartproperty_secret_key'  # Required for flash messages

# ✅ Register Blueprints
app.register_blueprint(upload_module)
app.register_blueprint(print_pages_bp)
app.register_blueprint(smartview_share_bp)
app.register_blueprint(smartview_panel_bp)
app.register_blueprint(smartview_advanced_bp)
app.register_blueprint(extract_pages_bp)
app.register_blueprint(share_pages_bp)
app.register_blueprint(smartview_watermark_bp)
app.register_blueprint(report_admin_bp)
app.register_blueprint(upload_other_bp)
app.register_blueprint(view_others_bp)
app.register_blueprint(view_personal_print_bp)
app.register_blueprint(view_personal_share_bp)
app.register_blueprint(view_personal_advanced_bp)
app.register_blueprint(personal_view_bp)
app.register_blueprint(personal_action_bp)
app.register_blueprint(view_personal_bp)
app.register_blueprint(extract_personal_bp)
app.register_blueprint(print_personal_bp)
app.register_blueprint(share_personal_bp)
app.register_blueprint(watermark_personal_bp)
app.register_blueprint(login_bp)  # ✅ Flask app me register karo
# ✅ Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# ✅ Professional Home Page Route
@app.route('/')
def home():
    return render_template('home.html')  # Use template instead of plain HTML

if __name__ == '__main__':
    app.run(debug=True)
