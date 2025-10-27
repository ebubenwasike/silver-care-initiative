from flask import Flask, request, render_template, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash

# ------------------------------
# Initialize Flask app
# ------------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'secretkey'  # Required for sessions

# ------------------------------
# Database connection
# ------------------------------
db_config = {
    "host": "localhost",
    "user": "root",              # your MySQL username
    "password": "EbubeNwasike",  # your MySQL password
    "database": "silver_care_db"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# ------------------------------
# ROUTES
# ------------------------------

# HOMEPAGE
@app.route('/')
def index():
    return render_template('index.html')

# TEMPORARY ROUTE - GENERATE PASSWORD (ADD THIS)
@app.route('/generate_password')
def generate_password():
    password = "password123"  # Change this to whatever password you want
    hashed = generate_password_hash(password)
    return f"Hashed password for '{password}': <br><strong>{hashed}</strong>"

# LOGIN PAGE
# LOGIN PAGE - SIMPLE VERSION (NO HASHING)
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
            return redirect(url_for('staff'))
        else:
            flash('Incorrect email/password!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')


# STAFF DASHBOARD just updated
@app.route('/StaffPage')
def staff():
    if 'loggedin' not in session:
        return redirect(url_for('login'))

    # Get the current staff member's ID
    staff_id = session['id']
    
    # Fetch patients created by this staff member
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


# CREATE PATIENT FORM - FIXED VERSION
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
        created_by = session['id']   # ← nurse's ID

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


# SENIORS LOGIN - UPDATED
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
            session['patient_first_name'] = account['first_name']  # ADD THIS
            session['patient_last_name'] = account['last_name']    # ADD THIS
            flash('Login successful!', 'success')
            return redirect(url_for('SeniorPage'))
        else:
            flash('Invalid email or PHN.', 'danger')

    return render_template('SeniorLogin.html')

#SENIORS DASHBOARD :)
@app.route('/SeniorPage')
def SeniorPage():
    if 'patient_loggedin' not in session:
        return redirect(url_for('SeniorLogin'))
    
    # Pass the patient's actual name to the template
    return render_template('SeniorPage.html', 
                         email=session['patient_email'],
                         first_name=session['patient_first_name'],
                         last_name=session['patient_last_name'])


# LOGOUT - IMPROVED WITH SMART REDIRECT
@app.route('/logout')
def logout():
    # Check if it's a patient logging out
    is_patient = 'patient_loggedin' in session
    
    # Clear everything from session
    session.clear()
    
    flash('You have been logged out successfully.', 'info')
    
    # Redirect to appropriate login page
    if is_patient:
        return redirect(url_for('SeniorLogin'))  # Go to patient login
    else:
        return redirect(url_for('login'))        # Go to staff login
    

# ABOUT PAGE
@app.route('/about')
def about():
    return render_template('about.html')

# HOSPITALS PAGE  
@app.route('/hospitals')
def hospitals():
    return render_template('hospitals.html')

# COMMUNITY PAGE
@app.route('/community')
def community():
    return render_template('community.html')

# EXERCISE PAGE
@app.route('/exercise')
def exercise():
    return render_template('exercise.html')


# ------------------------------
# Run the app
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
