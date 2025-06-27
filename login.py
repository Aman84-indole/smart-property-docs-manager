from flask import Blueprint, render_template, request, redirect, session, flash

login_bp = Blueprint('login_bp', __name__)

# Dummy credentials
users = {
    'admin': {'username': 'admin', 'password': 'admin123'},
    'user': {'username': 'user', 'password': 'user123'}
}

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')  # ✅ safely get role from form

        # Validation
        if role in users and username == users[role]['username'] and password == users[role]['password']:
            session['username'] = username
            session['role'] = role
            flash('Login successful!', 'success')

            if role == 'admin':
                return redirect('/dashboard')
            else:
                return redirect('/user-dashboard')

        flash('Invalid credentials!', 'danger')
        return render_template('login.html', role=role)

    # For GET method
    role = request.args.get('role', '')
    return render_template('login.html', role=role)
