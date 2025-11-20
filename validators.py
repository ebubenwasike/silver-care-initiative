# validators.py
import re

def validate_name(name):
    """Validate first and last names - letters only, max 50 chars"""
    if not name or not isinstance(name, str):
        return False, "Name must be a string."
    if not name.replace(" ", "").isalpha() or len(name) > 50:
        return False, "Name must contain only letters and spaces (max 50 characters)."
    return True, ""

def validate_email(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False, "Email must be a string."
    
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        return False, "Invalid email format (e.g., example@email.com)."
    return True, ""

def validate_phone(phone):
    """Validate phone number - 10-15 digits"""
    if not phone or not isinstance(phone, str):
        return False, "Phone number must be a string."
    
    # Remove any non-digit characters
    clean_phone = re.sub(r'\D', '', phone)
    if not clean_phone.isdigit() or not 10 <= len(clean_phone) <= 15:
        return False, "Phone number must contain 10–15 digits."
    return True, ""

def validate_age(age):
    """Validate age between 40 and 60"""
    if not age:
        return False, "Age is required."
    
    try:
        age_int = int(age)
        if not 40 <= age_int <= 60:
            return False, "Age must be between 40 and 60."
    except (ValueError, TypeError):
        return False, "Age must be a valid integer."
    return True, ""

def validate_heart_rate(hr):
    """Validate heart rate between 40-180 bpm"""
    if not hr:
        return False, "Heart rate is required."
    
    try:
        hr_int = int(hr)
        if not 40 <= hr_int <= 180:
            return False, "Heart rate must be between 40–180 bpm."
    except (ValueError, TypeError):
        return False, "Heart rate must be a valid integer."
    return True, ""

def validate_respiratory_rate(rr):
    """Validate respiratory rate between 10-30 breaths/min"""
    if not rr:
        return False, "Respiratory rate is required."
    
    try:
        rr_int = int(rr)
        if not 10 <= rr_int <= 30:
            return False, "Respiratory rate must be between 10–30 breaths/min."
    except (ValueError, TypeError):
        return False, "Respiratory rate must be a valid integer."
    return True, ""

def validate_blood_pressure(bp):
    """Validate blood pressure format (Systolic/Diastolic) and ranges"""
    if not bp:
        return False, "Blood pressure is required."
    
    try:
        if '/' not in bp:
            return False, "Blood pressure format must be Systolic/Diastolic (e.g., 120/80)."
        
        systolic, diastolic = map(int, bp.split('/'))
        if not (80 <= systolic <= 200):
            return False, "Systolic blood pressure must be between 80–200."
        if not (50 <= diastolic <= 130):
            return False, "Diastolic blood pressure must be between 50–130."
    except (ValueError, TypeError, IndexError):
        return False, "Blood pressure format invalid. Use Systolic/Diastolic (e.g., 120/80)."
    return True, ""

def validate_bmi(bmi):
    """Validate BMI between 10 and 50"""
    if not bmi:
        return True, ""  # BMI is optional
    
    try:
        bmi_float = float(bmi)
        if not 10 <= bmi_float <= 50:
            return False, "BMI must be between 10 and 50."
    except (ValueError, TypeError):
        return False, "BMI must be a valid number."
    return True, ""

def validate_weight(weight):
    """Validate weight between 30-200 kg"""
    if not weight:
        return True, ""  # Weight is optional
    
    try:
        weight_float = float(weight)
        if not 30 <= weight_float <= 200:
            return False, "Weight must be between 30–200 kg."
    except (ValueError, TypeError):
        return False, "Weight must be a valid number."
    return True, ""

def validate_height(height):
    """Validate height between 100-250 cm"""
    if not height:
        return True, ""  # Height is optional
    
    try:
        height_float = float(height)
        if not 100 <= height_float <= 250:
            return False, "Height must be between 100–250 cm."
    except (ValueError, TypeError):
        return False, "Height must be a valid number."
    return True, ""

def validate_temperature(temp):
    """Validate temperature between 35.0-42.0 °C"""
    if not temp:
        return False, "Temperature is required."
    
    try:
        temp_float = float(temp)
        if not 35.0 <= temp_float <= 42.0:
            return False, "Temperature must be between 35.0–42.0 °C."
    except (ValueError, TypeError):
        return False, "Temperature must be a valid number."
    return True, ""

def validate_password(pw):
    """Validate password strength"""
    if not pw or not isinstance(pw, str):
        return False, "Password must be a string."
    
    if len(pw) < 8:
        return False, "Password must be at least 8 characters long."
    
    # Check for uppercase, lowercase, digit, and special character
    has_upper = any(c.isupper() for c in pw)
    has_lower = any(c.islower() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(not c.isalnum() for c in pw)
    
    if not (has_upper and has_lower and has_digit and has_special):
        return False, "Password must include uppercase, lowercase, number, and special character."
    
    return True, ""

def get_valid_phn(phn, conn):
    """Clean and validate PHN (Personal Health Number)"""
    if not phn:
        return ""
    
    # Remove spaces and clean the PHN
    clean_phn = phn.strip().replace(" ", "").replace("-", "")
    return clean_phn
