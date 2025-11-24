import pytest
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from validators import *

class TestValidators:
    """Unit tests for all validator functions returning (bool, message) tuples"""
    
    def test_validate_name(self):
        """Test validate_name function"""
        success, message = validate_name("John")
        assert success == True
        assert message == ""
        
        success, message = validate_name("John123")
        assert success == False
        assert "letters" in message
        
        success, message = validate_name("")
        assert success == False
        assert message != ""

    def test_validate_email(self):
        """Test validate_email function"""
        success, message = validate_email("test@example.com")
        assert success == True
        assert message == ""
        
        success, message = validate_email("invalid")
        assert success == False
        assert "email" in message.lower()
        
        success, message = validate_email("")
        assert success == False
        assert message != ""

    def test_validate_phone(self):
        """Test validate_phone function"""
        success, message = validate_phone("1234567890")
        assert success == True
        assert message == ""
        
        success, message = validate_phone("123")
        assert success == False
        assert "digits" in message
        
        success, message = validate_phone("(123) 456-7890")
        assert success == True  # Should clean and validate

    def test_validate_age(self):
        """Test validate_age function"""
        success, message = validate_age("45")
        assert success == True
        assert message == ""
        
        success, message = validate_age("100")
        assert success == False
        assert "between" in message
        
        success, message = validate_age("25")
        assert success == False
        assert "between" in message
        
        success, message = validate_age("")
        assert success == False
        assert message != ""

    def test_validate_heart_rate(self):
        """Test validate_heart_rate function"""
        success, message = validate_heart_rate("72")
        assert success == True
        assert message == ""
        
        success, message = validate_heart_rate("200")
        assert success == False
        assert "40–180" in message
        
        success, message = validate_heart_rate("")
        assert success == False
        assert message != ""

    def test_validate_respiratory_rate(self):
        """Test validate_respiratory_rate function"""
        success, message = validate_respiratory_rate("16")
        assert success == True
        assert message == ""
        
        success, message = validate_respiratory_rate("5")
        assert success == False
        assert "10–30" in message
        
        success, message = validate_respiratory_rate("")
        assert success == False
        assert message != ""

    def test_validate_blood_pressure(self):
        """Test validate_blood_pressure function"""
        success, message = validate_blood_pressure("120/80")
        assert success == True
        assert message == ""
        
        success, message = validate_blood_pressure("12080")
        assert success == False
        assert "format" in message.lower()
        
        success, message = validate_blood_pressure("300/100")
        assert success == False
        assert "Systolic" in message or "Diastolic" in message
        
        success, message = validate_blood_pressure("")
        assert success == False
        assert message != ""

    def test_validate_bmi(self):
        """Test validate_bmi function"""
        success, message = validate_bmi("22.5")
        assert success == True
        assert message == ""
        
        success, message = validate_bmi("5")
        assert success == False
        assert "10 and 50" in message
        
        success, message = validate_bmi("")
        assert success == True  # BMI is optional
        assert message == ""

    def test_validate_weight(self):
        """Test validate_weight function"""
        success, message = validate_weight("70")
        assert success == True
        assert message == ""
        
        success, message = validate_weight("10")
        assert success == False
        assert "30–200" in message
        
        success, message = validate_weight("")
        assert success == True  # Weight is optional
        assert message == ""

    def test_validate_height(self):
        """Test validate_height function"""
        success, message = validate_height("175")
        assert success == True
        assert message == ""
        
        success, message = validate_height("50")
        assert success == False
        assert "100–250" in message
        
        success, message = validate_height("")
        assert success == True  # Height is optional
        assert message == ""

    def test_validate_temperature(self):
        """Test validate_temperature function"""
        success, message = validate_temperature("36.5")
        assert success == True
        assert message == ""
        
        success, message = validate_temperature("30.0")
        assert success == False
        assert "35.0–42.0" in message
        
        success, message = validate_temperature("")
        assert success == False
        assert message != ""

    def test_validate_password(self):
        """Test validate_password function"""
        success, message = validate_password("StrongPass123!")
        assert success == True
        assert message == ""
        
        success, message = validate_password("weak")
        assert success == False
        assert "8" in message or "characters" in message
        
        success, message = validate_password("nouppercase123!")
        assert success == False
        assert "uppercase" in message.lower()
        
        success, message = validate_password("")
        assert success == False
        assert message != ""

    def test_get_valid_phn(self):
        """Test get_valid_phn function"""
        # Mock connection object (not actually used in the function)
        class MockConn:
            pass
        
        conn = MockConn()
        
        # Test cleaning functionality
        clean_phn = get_valid_phn(" 123-456-789 ", conn)
        assert clean_phn == "123456789"
        
        clean_phn = get_valid_phn("", conn)
        assert clean_phn == ""

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
