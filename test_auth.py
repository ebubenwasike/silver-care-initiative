import pytest
import sys
import os

# Add th0e app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from validators import *

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client

# ===== VALIDATOR TESTS =====

def test_validate_name():
    """Test name validation"""
    assert validate_name("John") == True
    assert validate_name("Mary Jane") == True
    assert validate_name("") == False
    assert validate_name("A" * 51) == False
    assert validate_name("John123") == False

def test_validate_email():
    """Test email validation"""
    assert validate_email("test@example.com") == True
    assert validate_email("user.name@domain.co.uk") == True
    assert validate_email("invalid") == False
    assert validate_email("missing@domain") == False
    assert validate_email("") == False

def test_validate_phone():
    """Test phone number validation"""
    assert validate_phone("1234567890") == True
    assert validate_phone("+123456789012345") == True
    assert validate_phone("123") == False  # Too short
    assert validate_phone("1234567890123456") == False  # Too long
    assert validate_phone("abc") == False  # Not digits

def test_validate_age():
    """Test age validation"""
    assert validate_age("45") == True
    assert validate_age("40") == True
    assert validate_age("60") == True
    assert validate_age("39") == False  # Too young
    assert validate_age("61") == False  # Too old
    assert validate_age("abc") == False  # Not a number

def test_validate_heart_rate():
    """Test heart rate validation"""
    assert validate_heart_rate("72") == True
    assert validate_heart_rate("40") == True
    assert validate_heart_rate("180") == True
    assert validate_heart_rate("39") == False  # Too low
    assert validate_heart_rate("181") == False  # Too high
    assert validate_heart_rate("abc") == False

def test_validate_blood_pressure():
    """Test blood pressure validation"""
    assert validate_blood_pressure("120/80") == True
    assert validate_blood_pressure("80/50") == True
    assert validate_blood_pressure("200/130") == True
    assert validate_blood_pressure("12080") == False  # Missing slash
    assert validate_blood_pressure("79/50") == False  # Systolic too low
    assert validate_blood_pressure("120/49") == False  # Diastolic too low

def test_validate_password():
    """Test password validation"""
    assert validate_password("StrongPass123!") == True
    assert validate_password("Aa1!aaaa") == True  # Minimum length
    assert validate_password("weak") == False  # Too short
    assert validate_password("weakpassword") == False  # No uppercase/digit/special
    assert validate_password("WEAKPASSWORD123") == False  # No lowercase/special
    assert validate_password("WeakPassword") == False  # No digit/special

def test_validate_temperature():
    """Test temperature validation"""
    assert validate_temperature("36.5") == True
    assert validate_temperature("35.0") == True
    assert validate_temperature("42.0") == True
    assert validate_temperature("34.9") == False  # Too low
    assert validate_temperature("42.1") == False  # Too high
    assert validate_temperature("abc") == False

# ===== AUTHENTICATION TESTS =====

def test_login_page_loads(client):
    """Test that login page loads successfully"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_senior_login_page_loads(client):
    """Test that senior login page loads successfully"""
    response = client.get('/SeniorLogin')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_staff_dashboard_requires_login(client):
    """Test that staff dashboard redirects when not logged in"""
    response = client.get('/StaffPage', follow_redirects=True)
    assert response.status_code == 200
    # Should redirect to login page
    assert b'Login' in response.data or b'login' in response.data

def test_create_patient_requires_login(client):
    """Test that create patient page requires login"""
    response = client.get('/CreatePatientForm', follow_redirects=True)
    assert response.status_code == 200
    # Should redirect to login page
    assert b'Login' in response.data or b'login' in response.data

def test_home_page_loads(client):
    """Test that home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200

def test_logout_redirects(client):
    """Test logout functionality"""
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    # Should show logout message and redirect to login

def test_forgot_password_page_loads(client):
    """Test forgot password page loads"""
    response = client.get('/forgot_password_page')
    assert response.status_code == 200
    assert b'Forgot Password' in response.data or b'Password' in response.data

# ===== FORM VALIDATION TESTS =====

def test_invalid_email_login(client):
    """Test login with invalid email format"""
    response = client.post('/login', data={
        'email': 'invalid-email',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    # Should show error message

def test_empty_login_fields(client):
    """Test login with empty fields"""
    response = client.post('/login', data={
        'email': '',
        'password': ''
    }, follow_redirects=True)
    assert response.status_code == 200

# ===== SESSION TESTS =====

def test_session_management(client):
    """Test basic session functionality"""
    with client.session_transaction() as session:
        session['test_key'] = 'test_value'
    
    # Access session in another context
    with client.session_transaction() as session:
        assert session.get('test_key') == 'test_value'

# ===== ERROR HANDLING TESTS =====

def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/nonexistent-page')
    assert response.status_code == 404

def test_method_not_allowed(client):
    """Test method not allowed handling"""
    response = client.post('/')  # POST to GET-only route
    assert response.status_code == 405

# ===== INTEGRATION TESTS =====

def test_password_hashing():
    """Test password hashing functionality"""
    from werkzeug.security import generate_password_hash, check_password_hash
    
    password = "TestPass123!"
    hashed = generate_password_hash(password)
    
    # Should verify correctly
    assert check_password_hash(hashed, password) == True
    # Should fail with wrong password
    assert check_password_hash(hashed, "WrongPass") == False

def test_validator_imports():
    """Test that all validators can be imported and are callable"""
    validators = [
        validate_name, validate_email, validate_phone, validate_age,
        validate_heart_rate, validate_respiratory_rate, validate_blood_pressure,
        validate_bmi, validate_weight, validate_height, validate_password,
        validate_temperature, get_valid_phn
    ]
    
    for validator in validators:
        assert callable(validator), f"{validator.__name__} is not callable"

# ===== EDGE CASE TESTS =====

def test_edge_case_names():
    """Test edge cases for name validation"""
    assert validate_name("A") == True  # Single character
    assert validate_name("O'Neil") == False  # Apostrophe not allowed
    assert validate_name("Jean-Luc") == False  # Hyphen not allowed
    assert validate_name("  ") == False  # Only spaces

def test_edge_case_emails():
    """Test edge cases for email validation"""
    assert validate_email("a@b.c") == True  # Minimal valid email
    assert validate_email("test@sub.domain.com") == True
    assert validate_email("test+tag@example.com") == True
    assert validate_email("@example.com") == False  # Missing local part
    assert validate_email("test@") == False  # Missing domain

def test_edge_case_passwords():
    """Test edge cases for password validation"""
    # Exactly 8 characters with all requirements
    assert validate_password("Aa1!aaaa") == True
    # 7 characters (too short)
    assert validate_password("Aa1!aaa") == False

if __name__ == "__main__":
    pytest.main([__file__, "-v"])