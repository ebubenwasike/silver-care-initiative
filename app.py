from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask import jsonify
import datetime #for live updates with time on vitals i think
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash #for hashing
import pyotp #these are for 2 factor auth w microsoft
import qrcode
import io
from flask import send_file


# ------------------------------
# Initialize Flask app
# ------------------------------
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'secretkey'  # Required for sessions

# ------------------------------
# Database connection
# ------------------------------
db_config = {
    "host": "127.0.0.1",
    "user": "root",              # MySQL username
    "password": "jewelSQL123",  # MySQL password
    "database": "mydatabase", #change db name from silver_care_db to mydatabase
    "port": 3306,
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

# LOGIN PAGE for staff
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM staff WHERE email=%s", (email,))
        account = cursor.fetchone()
        cursor.close()
        conn.close()

        # 1️⃣ check if account exists
        if not account:
            flash('Incorrect email or password!', 'danger')
            return redirect(url_for('login'))

        # 2️⃣ verify password (hashed or plain)
        stored_pw = account['password']
        valid_pw = False
        if stored_pw == password or check_password_hash(stored_pw, password):
            valid_pw = True

        if not valid_pw:
            flash('Incorrect email or password!', 'danger')
            return redirect(url_for('login'))

        # 3️⃣ store session temporarily until 2FA verification
        session['pending_staff_id'] = account['id']
        session['pending_email'] = account['email']

        # 4️⃣ handle 2FA setup or verification
        if not account['totp_secret']:
            # redirect to setup 2FA if secret missing
            return redirect(url_for('setup_2fa', staff_id=account['id']))
        else:
            # prompt user for 2FA code
            return render_template('verify_2fa.html', email=email)

    # 5️⃣ initial GET request → show login page
    return render_template('login.html')


# SETUP 2FA (FIRST TIME)
@app.route('/setup_2fa/<int:staff_id>')
def setup_2fa(staff_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff WHERE id=%s", (staff_id,))
    staff = cursor.fetchone()

    if not staff:
        flash("Staff not found.", "danger")
        return redirect(url_for('login'))

    # Generate a new secret and save it
    secret = pyotp.random_base32()
    cursor.execute("UPDATE staff SET totp_secret=%s WHERE id=%s", (secret, staff_id))
    conn.commit()
    cursor.close()
    conn.close()

    # Create provisioning URI
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=staff['email'], issuer_name="SilverCare")

    # Generate QR code
    img = qrcode.make(uri)
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)

    return send_file(buf, mimetype='image/png')
    


# VERIFY 2FA CODE
@app.route('/verify_2fa', methods=['POST'])
def verify_2fa():
    code = request.form['code']  # The 6-digit code entered by staff
    staff_id = session.get('pending_staff_id')

    if not staff_id:
        flash("Session expired. Please log in again.", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM staff WHERE id=%s", (staff_id,))
    staff = cursor.fetchone()
    cursor.close()
    conn.close()

    if not staff:
        flash("Staff not found.", "danger")
        return redirect(url_for('login'))

    totp = pyotp.TOTP(staff['totp_secret'])

    # Verify the entered code
    if totp.verify(code):
        # 2FA success → fully log in
        session.pop('pending_staff_id', None)
        session.pop('pending_email', None)
        session['loggedin'] = True
        session['id'] = staff['id']
        session['email'] = staff['email']
        return redirect(url_for('staff'))
    else:
        flash('Invalid or expired 2FA code.', 'danger')
        return render_template('verify_2fa.html', email=staff['email'])


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


# SENIOR LOGIN
@app.route('/SeniorLogin', methods=['GET', 'POST'])
def SeniorLogin():
    if request.method == 'POST':
        email = request.form['email']
        phn_or_password = request.form['phn']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients WHERE email=%s", (email,))
        account = cursor.fetchone()
        cursor.close()
        conn.close()

        if account:
            # Allow login by PHN or password
            if account['phn'] == phn_or_password or (
                account.get('password') and check_password_hash(account['password'], phn_or_password)
            ):
                session['patient_loggedin'] = True
                session['patient_id'] = account['id']
                session['patient_email'] = account['email']
                session['patient_first_name'] = account['first_name']
                session['patient_last_name'] = account['last_name']
                flash('Login successful!', 'success')
                return redirect(url_for('SeniorPage'))

        flash('Invalid email or PHN/password.', 'danger')

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


 #APPOINTMENT BOOKING <333!    
@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    try:
        # Check if staff is logged in
        if 'loggedin' in session:
            patient_id = request.form['patient_id']
            staff_id = session['id']
            
            # Verify the patient belongs to this staff
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM patients WHERE id=%s AND created_by=%s", (patient_id, staff_id))
            patient = cursor.fetchone()
            
            if not patient:
                return jsonify(success=False, error='Patient not found or not assigned to you')
                
        # Check if patient is logged in
        elif 'patient_loggedin' in session:
            patient_id = session['patient_id']
            
            # Get the staff who created this patient
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT created_by FROM patients WHERE id=%s", (patient_id,))
            patient_data = cursor.fetchone()
            
            if not patient_data:
                return jsonify(success=False, error='Patient not found')
                
            staff_id = patient_data[0]
            
        else:
            return jsonify(success=False, error='Not logged in')
        
        # Common appointment data
        appointment_date = request.form['appointment_date']
        appointment_time = request.form['appointment_time']
        appointment_type = request.form['appointment_type']
        notes = request.form.get('notes', '')
        
        # Insert appointment
        cursor.execute("""
            INSERT INTO appointments (patient_id, staff_id, appointment_date, appointment_time, appointment_type, notes, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'scheduled')
        """, (patient_id, staff_id, appointment_date, appointment_time, appointment_type, notes))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, error=str(e))

#get patient appt
@app.route('/get_patient_appointments')
def get_patient_appointments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        patient_id = session.get('patient_id')

        cursor.execute("""
            SELECT 
                a.id, 
                a.appointment_date, 
                a.appointment_time, 
                a.appointment_type, 
                a.status, 
                a.notes,
                s.first_name AS staff_first_name, 
                s.last_name AS staff_last_name
            FROM appointments a
            JOIN staff s ON a.staff_id = s.id
            WHERE a.patient_id = %s
            ORDER BY a.appointment_date DESC, a.appointment_time ASC
        """, (patient_id,))

        appointments = cursor.fetchall()

        for appt in appointments:
            if isinstance(appt['appointment_date'], (datetime.date, datetime.datetime)):
                appt['appointment_date'] = appt['appointment_date'].strftime('%Y-%m-%d')
            if isinstance(appt['appointment_time'], (datetime.time, datetime.timedelta)):
                appt['appointment_time'] = str(appt['appointment_time'])

        cursor.close()
        conn.close()

        return jsonify(success=True, appointments=appointments)
    except Exception as e:
        print("❌ Error fetching patient appointments:", e)
        return jsonify(success=False, error=str(e))



#get staff appointments
@app.route('/get_staff_appointments')
def get_staff_appointments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        staff_id = session.get('id')  # or your actual staff session key

        cursor.execute("""
            SELECT 
                a.id, 
                a.appointment_date, 
                a.appointment_time, 
                a.appointment_type, 
                a.status, 
                a.notes,
                p.first_name, 
                p.last_name
            FROM appointments a
            JOIN patients p ON a.patient_id = p.id
            WHERE a.staff_id = %s
            ORDER BY a.appointment_date DESC, a.appointment_time ASC
        """, (staff_id,))

        appointments = cursor.fetchall()

        # 🔹 Convert date/time to string so Flask can jsonify it
        for appt in appointments:
            if isinstance(appt['appointment_date'], (datetime.date, datetime.datetime)):
                appt['appointment_date'] = appt['appointment_date'].strftime('%Y-%m-%d')
            if isinstance(appt['appointment_time'], (datetime.time, datetime.timedelta)):
                appt['appointment_time'] = str(appt['appointment_time'])

        cursor.close()
        conn.close()

        return jsonify(success=True, appointments=appointments)
    except Exception as e:
        print("❌ Error fetching staff appointments:", e)
        return jsonify(success=False, error=str(e))

#DELETE APPOINTMENTS
@app.route('/delete_appointment/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True, message="Appointment deleted successfully")
    except Exception as e:
        print("❌ Error deleting appointment:", e)
        return jsonify(success=False, error=str(e))


#ADD/UPDATE VITALS <3!!
@app.route('/update_vitals', methods=['POST'])
def update_vitals():
    try:
        patient_id = request.form['patient_id']
        staff_id = session.get('id')  # staff updating it

        blood_pressure = request.form.get('blood_pressure')
        bmi = request.form.get('bmi')
        weight = request.form.get('weight')
        height = request.form.get('height')
        respiratory_rate = request.form.get('respiratory_rate')
        temperature = request.form.get('temperature')
        heart_rate = request.form.get('heart_rate')

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if vitals exist for this patient already
        cursor.execute("SELECT id FROM vitals WHERE patient_id = %s", (patient_id,))
        existing = cursor.fetchone()

        if existing:
            cursor.execute("""
                UPDATE vitals
                SET blood_pressure=%s, bmi=%s, weight=%s, height=%s,
                    respiratory_rate=%s, temperature=%s, heart_rate=%s, staff_id=%s
                WHERE patient_id=%s
            """, (blood_pressure, bmi, weight, height, respiratory_rate, temperature, heart_rate, staff_id, patient_id))
        else:
            cursor.execute("""
                INSERT INTO vitals (patient_id, staff_id, blood_pressure, bmi, weight, height, respiratory_rate, temperature, heart_rate)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (patient_id, staff_id, blood_pressure, bmi, weight, height, respiratory_rate, temperature, heart_rate))
            
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True)
    except Exception as e:
        print("❌ Error updating vitals:", e)
        return jsonify(success=False, error=str(e))

#GET VITALS (STAFF AND SENIORS)
@app.route('/get_vitals/<int:patient_id>')
def get_vitals(patient_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT blood_pressure, bmi, weight, height, respiratory_rate, temperature, heart_rate,
                   DATE_FORMAT(updated_at, '%%Y-%%m-%%d %%H:%%i') AS updated_at
            FROM vitals
            WHERE patient_id = %s
            ORDER BY updated_at DESC
            LIMIT 1
        """, (patient_id,))

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return jsonify(success=True, vitals=result)
        else:
            return jsonify(success=False, vitals=None)
    except Exception as e:
        print("❌ Error fetching vitals:", e)
        return jsonify(success=False, error=str(e))

# FORGOT PASSWORD
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Try staff first
    cursor.execute("SELECT security_question FROM staff WHERE email=%s", (email,))
    user = cursor.fetchone()

    # If not found, try patients
    if not user:
        cursor.execute("SELECT security_question FROM patients WHERE email=%s", (email,))
        user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        print(f"📩 Forgot password request for {email}")
        return jsonify({'success': True, 'question': user['security_question']})
    else:
        print(f"❌ Email not found: {email}")
        return jsonify({'success': False})


# VERIFY SECURITY
@app.route('/verify_security', methods=['POST'])
def verify_security():
    data = request.get_json()
    email = data.get('email')
    answer = data.get('answer')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Try staff first
    cursor.execute("SELECT id FROM staff WHERE email=%s AND security_answer=%s", (email, answer))
    user = cursor.fetchone()

    # If not found, try patients
    if not user:
        cursor.execute("SELECT id FROM patients WHERE email=%s AND security_answer=%s", (email, answer))
        user = cursor.fetchone()

    cursor.close()
    conn.close()

    return jsonify({'success': bool(user)})

# RESET PASSWORD
@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    email = data.get('email')
    new_password = data.get('new_password')
    hashed_pw = generate_password_hash(new_password)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Update staff password
    cursor.execute("UPDATE staff SET password=%s WHERE email=%s", (hashed_pw, email))
    # Update patient password
    cursor.execute("UPDATE patients SET password=%s WHERE email=%s", (hashed_pw, email))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"✅ Password successfully reset for {email}")
    return jsonify({'success': True})


#SET SECURITY QUESTION
@app.route('/set_security', methods=['POST'])
def set_security():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')

    conn = get_db_connection()
    cursor = conn.cursor()

    # For staff
    if 'loggedin' in session:
        cursor.execute("""
            UPDATE staff 
            SET security_question = %s, security_answer = %s 
            WHERE id = %s
        """, (question, answer, session['id']))

    # For seniors
    elif 'patient_loggedin' in session:
        cursor.execute("""
            UPDATE patients 
            SET security_question = %s, security_answer = %s 
            WHERE id = %s
        """, (question, answer, session['patient_id']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'success': True})


#CHANGE PASSWORD BUTTON
@app.route('/change_password', methods=['POST'])
def change_password():
    if 'loggedin' not in session and 'patient_loggedin' not in session:
        return jsonify({'success': False, 'message': 'Not logged in.'})

    data = request.get_json()
    security_answer = data.get('answer')
    new_password = data.get('new_password')
    hashed_pw = generate_password_hash(new_password)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Check whether it's staff or patient
    if 'loggedin' in session:
        cursor.execute("SELECT security_answer FROM staff WHERE id=%s", (session['id'],))
        user = cursor.fetchone()
        if user and user['security_answer'].lower() == security_answer.lower():
            cursor.execute("UPDATE staff SET password=%s WHERE id=%s", (hashed_pw, session['id']))
    elif 'patient_loggedin' in session:
        cursor.execute("SELECT security_answer FROM patients WHERE id=%s", (session['patient_id'],))
        user = cursor.fetchone()
        if user and user['security_answer'].lower() == security_answer.lower():
            cursor.execute("UPDATE patients SET password=%s WHERE id=%s", (hashed_pw, session['patient_id']))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'success': True})

#GET SECURITY QUESTION for change password function
@app.route('/get_security_question')
def get_security_question():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if 'loggedin' in session:
        cursor.execute("SELECT security_question FROM staff WHERE id=%s", (session['id'],))
    elif 'patient_loggedin' in session:
        cursor.execute("SELECT security_question FROM patients WHERE id=%s", (session['patient_id'],))
    else:
        return jsonify({'success': False})
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'question': result['security_question'] if result else 'None'})


#FORG PASSWORD PAGE
@app.route('/forgot_password_page')
def forgot_password_page():
    return render_template('ForgotPassword.html')



#HASH STUFF (TEMPORARY)

@app.route('/rehash_staff_passwords')
def rehash_staff_passwords():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, password FROM staff")
    staff_accounts = cursor.fetchall()

    updated = 0
    for acc in staff_accounts:
        pw = acc['password']
        # Skip if already hashed
        if not pw.startswith('pbkdf2:sha256'):
            hashed_pw = generate_password_hash(pw)
            cursor2 = conn.cursor()
            cursor2.execute("UPDATE staff SET password=%s WHERE id=%s", (hashed_pw, acc['id']))
            cursor2.close()
            updated += 1

    conn.commit()
    cursor.close()
    conn.close()
    return f"✅ Rehashed {updated} plain-text staff passwords!"


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

@app.route('/debug_patients')
def debug_patients():
    if 'loggedin' not in session:
        return "Not logged in"
    
    staff_id = session['id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients WHERE created_by = %s LIMIT 1", (staff_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return f"Patient data: {patient}"


# ------------------------------
# Run the app
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
