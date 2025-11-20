import pytest
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class TestAuthRoutes:
    """Unit tests for authentication routes"""
    
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

    def test_create_patient_requires_login(self, client):
        """Test that create patient page requires login"""
        response = client.get('/CreatePatientForm', follow_redirects=True)
        assert response.status_code == 200

    def test_home_page_accessible(self, client):
        """Test that home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200

    def test_logout_redirects(self, client):
        """Test logout functionality"""
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200

    def test_forgot_password_page_accessible(self, client):
        """Test forgot password page loads"""
        response = client.get('/forgot_password_page')
        assert response.status_code == 200

    def test_about_page_accessible(self, client):
        """Test about page loads"""
        response = client.get('/about')
        assert response.status_code == 200

    def test_hospitals_page_accessible(self, client):
        """Test hospitals page loads"""
        response = client.get('/hospitals')
        assert response.status_code == 200

    def test_community_page_accessible(self, client):
        """Test community page loads"""
        response = client.get('/community')
        assert response.status_code == 200

    def test_exercise_page_accessible(self, client):
        """Test exercise page loads"""
        response = client.get('/exercise')
        assert response.status_code == 200
