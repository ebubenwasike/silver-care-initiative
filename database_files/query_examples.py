from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    _tablename_ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'senior' or 'nurse'
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def _repr_(self):
        return f'<User {self.email} - {self.role}>'

class Appointment(db.Model):
    _tablename_ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    senior_id = db.Column(db.Integer, nullable=False)
    nurse_id = db.Column(db.Integer, nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def _repr_(self):
        return f'<Appointment {self.id}>'

class HealthRecord(db.Model):
    _tablename_ = 'health_records'
    
    id = db.Column(db.Integer, primary_key=True)
    senior_id = db.Column(db.Integer, nullable=False)
    recorded_by = db.Column(db.Integer, nullable=False)
    blood_pressure = db.Column(db.String(20))  # Store as "120/80"
    blood_sugar = db.Column(db.Float)  # in mmol/L
    oxygen_level = db.Column(db.Float)  # percentage
    body_temperature = db.Column(db.Float)  # Celsius
    weight = db.Column(db.Float)  # kg
    notes = db.Column(db.Text)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    
    def _repr_(self):
        return f'<HealthRecord {self.id}>'

class EmergencyContact(db.Model):
    _tablename_ = 'emergency_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    senior_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    priority = db.Column(db.Integer, default=1)  # 1 = primary, 2 = secondary
    
    def _repr_(self):
        return f'<EmergencyContact {self.name}>'