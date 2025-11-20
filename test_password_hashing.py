import pytest
from werkzeug.security import generate_password_hash, check_password_hash

class TestPasswordHashing:
    """Unit tests for password hashing functionality"""
    
    def test_password_hashing_works(self):
        """Test that password hashing and verification works"""
        password = "TestPass123!"
        hashed = generate_password_hash(password)
        
        # Should verify correctly with correct password
        assert check_password_hash(hashed, password) == True
        
        # Should fail with wrong password
        assert check_password_hash(hashed, "WrongPass") == False
        
        # Should fail with empty password
        assert check_password_hash(hashed, "") == False

    def test_different_passwords_produce_different_hashes(self):
        """Test that different passwords produce different hashes"""
        password1 = "Password123!"
        password2 = "Password124!"
        
        hashed1 = generate_password_hash(password1)
        hashed2 = generate_password_hash(password2)
        
        assert hashed1 != hashed2