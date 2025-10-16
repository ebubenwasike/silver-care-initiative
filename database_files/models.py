from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    _tablename_ = 'users'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User Information
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'senior' or 'nurse'
    
    # Timestamps
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Password methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def _repr_(self):
        return f'<User {self.email} - {self.role}>'

class Appointment(db.Model):
    _tablename_ = 'appointments'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    senior_id = db.Column(db.Integer, nullable=False)
    nurse_id = db.Column(db.Integer, nullable=False)
    
    # Appointment Details
    appointment_date = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled
    notes = db.Column(db.Text)
    
    # Timestamps
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<Appointment {self.id} - {self.appointment_date}>'

class HealthRecord(db.Model):
    _tablename_ = 'health_records'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    senior_id = db.Column(db.Integer, nullable=False)
    recorded_by = db.Column(db.Integer, nullable=False)  # Nurse ID
    
    # Health Metrics
    blood_pressure_systolic = db.Column(db.Integer)  # Upper number
    blood_pressure_diastolic = db.Column(db.Integer) # Lower number
    blood_sugar = db.Column(db.Float)  # mmol/L
    oxygen_level = db.Column(db.Float) # Percentage
    body_temperature = db.Column(db.Float)  # Celsius
    weight = db.Column(db.Float)  # kg
    heart_rate = db.Column(db.Integer)  # BPM
    
    # Additional Info
    notes = db.Column(db.Text)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)
    
    def _repr_(self):
        return f'<HealthRecord {self.id} - Senior {self.senior_id}>'

class EmergencyContact(db.Model):
    _tablename_ = 'emergency_contacts'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    senior_id = db.Column(db.Integer, nullable=False)
    
    # Contact Information
    name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    
    # Priority and Status
    priority = db.Column(db.Integer, default=1)  # 1 = primary, 2 = secondary
    is_active = db.Column(db.Boolean, default=True)
    
    def _repr_(self):
        return f'<EmergencyContact {self.name} - {self.relationship}>'

class Medication(db.Model):
    _tablename_ = 'medications'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    senior_id = db.Column(db.Integer, nullable=False)
    
    # Medication Details
    name = db.Column(db.String(100), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)  # 'daily', 'twice daily', etc.
    time_of_day = db.Column(db.String(50))  # 'morning', 'evening', 'bedtime'
    instructions = db.Column(db.Text)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    
    def _repr_(self):
        return f'<Medication {self.name} - {self.dosage}>'

class CommunityEvent(db.Model):
    _tablename_ = 'community_events'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Event Details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100))
    event_type = db.Column(db.String(50))  # 'exercise', 'social', 'educational'
    
    # Management
    created_by = db.Column(db.Integer, nullable=False)  # Nurse ID
    max_participants = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def _repr_(self):
        return f'<CommunityEvent {self.title} - {self.event_date}>'