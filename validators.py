# validators.py
import re

def validate_name(name):
    """Validate first and last names - letters only, max 50 chars"""
    if not name or not isinstance(name, str):
        return False
    if not name.replace(" ", "").isalpha() or len(name) > 50:
        return False
    return True

def validate_email(email):
    """Validate email format"""
    if not email or not isinstance(email, str):
        return False
    
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        return False
    return True

def validate_phone(phone):
    """Validate phone number - 10-15 digits"""
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove any non-digit characters
    clean_phone = re.sub(r'\D', '', phone)
    if not clean_phone.isdigit() or not 10 <= len(clean_phone) <= 15:
        return False
    return True

def validate_age(age):
    """Validate age between 40 and 60"""
    if not age:
        return False
    
    try:
        age_int = int(age)
        if not 40 <= age_int <= 60:
            return False
    except (ValueError, TypeError):
        return False
    return True

def validate_heart_rate(hr):
    """Validate heart rate between 40-180 bpm"""
    if not hr:
        return False
    
    try:
        hr_int = int(hr)
        if not 40 <= hr_int <= 180:
            return False
    except (ValueError, TypeError):
        return False
    return True

def validate_respiratory_rate(rr):
    """Validate respiratory rate between 10-30 breaths/min"""
    if not rr:
        return False
    
    try:
        rr_int = int(rr)
        if not 10 <= rr_int <= 30:
            return False
    except (ValueError, TypeError):
        return False
    return True

def validate_blood_pressure(bp):
    """Validate blood pressure format (Systolic/Diastolic) and ranges"""
    if not bp:
        return False
    
    try:
        if '/' not in bp:
            return False
        
        systolic, diastolic = map(int, bp.split('/'))
        if not (80 <= systolic <= 200):
            return False
        if not (50 <= diastolic <= 130):
            return False
    except (ValueError, TypeError, IndexError):
        return False
    return True

def validate_bmi(bmi):
    """Validate BMI between 10 and 50"""
    if not bmi:
        return True  # BMI is optional
    
    try:
        bmi_float = float(bmi)
        if not 10 <= bmi_float <= 50:
            return False
    except (ValueError, TypeError):
        return False
    return True

def validate_weight(weight):
    """Validate weight between 30-200 kg"""
    if not weight:
        return True  # Weight is optional
    
    try:
        weight_float = float(weight)
        if not 30 <= weight_float <= 200:
            return False
    except (ValueError, TypeError):
        return False
    return True

def validate_height(height):
    """Validate height between 100-250 cm"""
    if not height:
        return True  # Height is optional
    
    try:
        height_float = float(height)
        if not 100 <= height_float <= 250:
            return False
    except (ValueError, TypeError):
        return False
    return True

def validate_temperature(temp):
    """Validate temperature between 35.0-42.0 °C"""
    if not temp:
        return False
    
    try:
        temp_float = float(temp)
        if not 35.0 <= temp_float <= 42.0:
            return False
    except (ValueError, TypeError):
        return False
    return True

def validate_password(pw):
    """Validate password strength"""
    if not pw or not isinstance(pw, str):
        return False
    
    if len(pw) < 8:
        return False
    
    # Check for uppercase, lowercase, digit, and special character
    has_upper = any(c.isupper() for c in pw)
    has_lower = any(c.islower() for c in pw)
    has_digit = any(c.isdigit() for c in pw)
    has_special = any(not c.isalnum() for c in pw)
    
    if not (has_upper and has_lower and has_digit and has_special):
        return False
    
    return True

def get_valid_phn(phn, conn):
    """Clean and validate PHN (Personal Health Number)"""
    if not phn:
        return ""
    
    # Remove spaces and clean the PHN
    clean_phn = phn.strip().replace(" ", "").replace("-", "")
    return clean_phn