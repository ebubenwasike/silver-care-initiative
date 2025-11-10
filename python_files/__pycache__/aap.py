from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import mysql.connector
# === SESSION TIMEOUT: Import for time tracking ===
from datetime import datetime, timedelta

# ------------------------------
# Initialize Flask app
# ------------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'silvercare_secret_key_2024'

# === SESSION TIMEOUT: Configure 30-minute session lifetime ===
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

# ------------------------------
# Database configuration
# ------------------------------
db_config = {
    "host": "localhost",
    "user": "root",              # MySQL username
    "password": "EbubeNwasike",  # MySQL password
    "database": "silver_care_db"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# === SESSION TIMEOUT: Middleware to check session activity ===
@app.before_request
def check_session_timeout():
    """Check and update session activity for timeout"""
    if any(key in session for key in ['loggedin', 'patient_loggedin']):
        session.permanent = True
        last_activity = session.get('last_activity')
        if last_activity:
            try:
                last_activity_dt = datetime.fromisoformat(last_activity)
                time_diff = datetime.now() - last_activity_dt
                # === SESSION TIMEOUT: Logout after 30 minutes inactivity ===
                if time_diff.total_seconds() > 1800:
                    session.clear()
                    if request.endpoint and request.endpoint != 'index':
                        flash('Your session has expired due to inactivity. Please log in again.', 'warning')
                    return redirect(url_for('index'))
            except ValueError:
                session.clear()
                return redirect(url_for('index'))
        # === SESSION TIMEOUT: Update activity timestamp on every request ===
        session['last_activity'] = datetime.now().isoformat()

# === SESSION TIMEOUT: API endpoint for frontend session checks ===
@app.route('/session-check')
def session_check():
    """API endpoint for frontend to check session status"""
    if 'loggedin' in session:
        minutes_remaining = 30 - int((datetime.now() - datetime.fromisoformat(session.get('last_activity'))).total_seconds() / 60)
        return jsonify({
            'logged_in': True,
            'user_type': 'staff',
            'minutes_remaining': max(0, minutes_remaining)
        })
    elif 'patient_loggedin' in session:
        minutes_remaining = 30 - int((datetime.now() - datetime.fromisoformat(session.get('last_activity'))).total_seconds() / 60)
        return jsonify({
            'logged_in': True,
            'user_type': 'patient',
            'minutes_remaining': max(0, minutes_remaining)
        })
    else:
        return jsonify({'logged_in': False})

# ------------------------------
# ROUTES
# ------------------------------

# HOMEPAGE
@app.route('/')
def index():
    return render_template('index.html')

# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM staff WHERE email=%s AND password=%s", (email, password))
        account = cursor.fetchone()
        cursor.close()
        conn.close()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['email'] = account['email']
            # === SESSION TIMEOUT: Initialize activity timestamp on login ===
            session['last_activity'] = datetime.now().isoformat()
            return redirect(url_for('staff'))
        else:
            flash('Incorrect email/password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# STAFF DASHBOARD
@app.route('/StaffPage')
def staff():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    staff_id = session['id']
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM patients 
        WHERE created_by = %s 
        ORDER BY created_at DESC
    """, (staff_id,))
    patients = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('StaffPage.html', patients=patients)

# CREATE PATIENT FORM
@app.route('/CreatePatientForm', methods=['GET', 'POST'])
def create_patient():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        dob = request.form['dob']
        phn = request.form['phn']
        emergency_contact = request.form['emergency_contact']
        created_by = session['id']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO patients (first_name, last_name, email, phone, dob, phn, emergency_contact, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, dob, phn, emergency_contact, created_by))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Patient account created successfully!', 'success')
        return redirect(url_for('staff'))

    return render_template('CreatePatientForm.html')

# SENIORS LOGIN 
@app.route('/SeniorLogin', methods=['GET', 'POST'])
def SeniorLogin():
    if request.method == 'POST':
        email = request.form['email']
        phn = request.form['phn']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients WHERE email=%s AND phn=%s", (email, phn))
        account = cursor.fetchone()
        cursor.close()
        conn.close()

        if account:
            session['patient_loggedin'] = True
            session['patient_id'] = account['id']
            session['patient_email'] = account['email']
            session['patient_first_name'] = account['first_name']
            session['patient_last_name'] = account['last_name']
            # === SESSION TIMEOUT: Initialize activity timestamp on login ===
            session['last_activity'] = datetime.now().isoformat()
            flash('Login successful!', 'success')
            return redirect(url_for('SeniorPage'))
        else:
            flash('Invalid email or PHN.', 'danger')

    return render_template('SeniorLogin.html')

# SENIORS DASHBOARD
@app.route('/SeniorPage')
def SeniorPage():
    if 'patient_loggedin' not in session:
        return redirect(url_for('SeniorLogin'))
    
    return render_template('SeniorPage.html', 
                         email=session['patient_email'],
                         first_name=session['patient_first_name'],
                         last_name=session['patient_last_name'])

# LOGOUT
@app.route('/logout')
def logout():
    user_type = 'Staff' if 'loggedin' in session else 'Senior'
    session.clear()
    flash(f'{user_type} logout successful!', 'info')
    return redirect(url_for('index'))

# ... REST OF YOUR EXISTING ROUTES REMAIN UNCHANGED ...
# (book_appointment, get_patient_appointments, get_staff_appointments, etc.)

# ------------------------------
# Run the app
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
