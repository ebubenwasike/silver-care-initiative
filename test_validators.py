import pytest
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from validators import *

class TestValidators:
    """Unit tests for validator functions returning (bool, message) tuples"""
    
    def test_validate_name_returns_tuple(self):
        success, message = validate_name("John")
        assert success == True
        assert message == ""
        
        success, message = validate_name("John123")
        assert success == False
        assert "letters" in message

    def test_validate_email_returns_tuple(self):
        success, message = validate_email("test@example.com")
        assert success == True
        assert message == ""
        
        success, message = validate_email("invalid")
        assert success == False
        assert "email" in message.lower()

    def test_validate_phone_returns_tuple(self):
        success, message = validate_phone("1234567890")
        assert success == True
        assert message == ""
        
        success, message = validate_phone("123")
        assert success == False
        assert "digits" in message

    def test_validate_age_returns_tuple(self):
        success, message = validate_age("45")
        assert success == True
        assert message == ""
        
        success, message = validate_age("100")
        assert success == False
        assert "between" in message

    def test_validate_password_returns_tuple(self):
        success, message = validate_password("StrongPass123!")
        assert success == True
        assert message == ""
        
        success, message = validate_password("weak")
        assert success == False
        assert "8" in message or "characters" in message

    def test_validate_blood_pressure_returns_tuple(self):
        success, message = validate_blood_pressure("120/80")
        assert success == True
        assert message == ""
        
        success, message = validate_blood_pressure("12080")
        assert success == False
        assert "format" in message.lower()

    def test_optional_fields_return_true_with_empty_message(self):
        # Test optional fields
        success, message = validate_bmi("")
        assert success == True
        assert message == ""
        
        success, message = validate_weight("")
        assert success == True
        assert message == ""
        
        success, message = validate_height("")
        assert success == True
        assert message == ""

    def test_required_fields_return_false_with_error_message(self):
        # Test required fields with empty values
        success, message = validate_name("")
        assert success == False
        assert message != ""
        
        success, message = validate_email("")
        assert success == False
        assert message != ""
        
        success, message = validate_age("")
        assert success == False
        assert message != ""

    def test_all_validators_return_tuples(self):
        """Test that all validators return (bool, message) tuples"""
        validators = [
            (validate_name, "John"),
            (validate_email, "test@example.com"),
            (validate_phone, "1234567890"),
            (validate_age, "45"),
            (validate_heart_rate, "72"),
            (validate_respiratory_rate, "16"),
            (validate_blood_pressure, "120/80"),
            (validate_bmi, "22.5"),
            (validate_weight, "70"),
            (validate_height, "175"),
            (validate_temperature, "36.5"),
            (validate_password, "Test123!"),
        ]
        
        for validator, test_value in validators:
            result = validator(test_value)
            assert isinstance(result, tuple), f"{validator.__name__} should return tuple"
            assert len(result) == 2, f"{validator.__name__} should return (bool, message)"
            assert isinstance(result[0], bool), f"{validator.__name__} first element should be bool"
            assert isinstance(result[1], str), f"{validator.__name__} second element should be str"