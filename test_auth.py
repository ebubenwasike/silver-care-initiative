
import pytest
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app as flask_app  # Import your Flask app

class TestAuthRoutes:
    """Unit tests for authentication routes"""
    
    @pytest.fixture
    def client(self):
        """Create a test client for the Flask app"""
        flask_app.config['TESTING'] = True
        with flask_app.test_client() as client:
            yield client

    def test_login_page_accessible(self, client):
        """Test that login page loads successfully"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data or b'login' in response.data

    def test_senior_login_page_accessible(self, client):
        """Test that senior login page loads successfully"""
        response = client.get('/SeniorLogin')
        assert response.status_code == 200
        assert b'Login' in response.data or b'login' in response.data

    def test_staff_dashboard_requires_login(self, client):
        """Test that staff dashboard redirects when not logged in"""
        response = client.get('/StaffPage', follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to login page
        assert b'Login' in response.data or b'login' in response.data

    def test_create_patient_requires_login(self, client):
        """Test that create patient page requires login"""
        response = client.get('/CreatePatientForm', follow_redirects=True)
        assert response.status_code == 200
        # Should redirect to login page
        assert b'Login' in response.data or b'login' in response.data

    def test_home_page_accessible(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'SilverCare' in response.data or b'Home' in response.data

    def test_logout_redirects(self, client):
        """Test logout functionality"""
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

    def test_forgot_password_page_accessible(self, client):
        """Test forgot password page loads"""
        response = client.get('/forgot_password_page')
        assert response.status_code == 200
        assert b'Forgot Password' in response.data or b'Password' in response.data

    def test_about_page_accessible(self, client):
        """Test about page loads"""
        response = client.get('/about')
        assert response.status_code == 200
        assert b'About' in response.data or b'about' in response.data

    def test_hospitals_page_accessible(self, client):
        """Test hospitals page loads"""
        response = client.get('/hospitals')
        assert response.status_code == 200
        assert b'Hospital' in response.data or b'hospital' in response.data

    def test_community_page_accessible(self, client):
        """Test community page loads"""
        response = client.get('/community')
        assert response.status_code == 200
        assert b'Community' in response.data or b'community' in response.data

    def test_exercise_page_accessible(self, client):
        """Test exercise page loads"""
        response = client.get('/exercise')
        assert response.status_code == 200
        assert b'Exercise' in response.data or b'exercise' in response.data
