from database.models import db, User, Appointment, HealthRecord, EmergencyContact, Medication, CommunityEvent
from datetime import datetime, timedelta

def create_sample_data(app):
    """Add comprehensive sample data to MySQL database"""
    with app.app_context():
        try:
            print("🗃 Starting to create sample data...")
            
            # Clear existing data (optional - for testing)
            db.session.query(Medication).delete()
            db.session.query(CommunityEvent).delete()
            db.session.query(EmergencyContact).delete()
            db.session.query(HealthRecord).delete()
            db.session.query(Appointment).delete()
            db.session.query(User).delete()
            
            # ========== CREATE USERS ==========
            print("👥 Creating sample users...")
            
            # Senior Users
            senior1 = User(
                email='john.senior@silvercare.com',
                first_name='John',
                last_name='Smith',
                role='senior'
            )
            senior1.set_password('password123')
            
            senior2 = User(
                email='mary.senior@silvercare.com',
                first_name='Mary',
                last_name='Johnson',
                role='senior'
            )
            senior2.set_password('password123')
            
            senior3 = User(
                email='robert.senior@silvercare.com',
                first_name='Robert',
                last_name='Brown',
                role='senior'
            )
            senior3.set_password('password123')
            
            # Nurse Users
            nurse1 = User(
                email='sarah.nurse@silvercare.com',
                first_name='Sarah',
                last_name='Wilson',
                role='nurse'
            )
            nurse1.set_password('password123')
            
            nurse2 = User(
                email='mike.nurse@silvercare.com',
                first_name='Mike',
                last_name='Davis',
                role='nurse'
            )
            nurse2.set_password('password123')
            
            # Add all users to session
            db.session.add_all([senior1, senior2, senior3, nurse1, nurse2])
            db.session.commit()
            print("✅ Users created successfully")
            
            # ========== CREATE APPOINTMENTS ==========
            print("📅 Creating sample appointments...")
            
            appointments = [
                Appointment(
                    senior_id=senior1.id,
                    nurse_id=nurse1.id,
                    appointment_date=datetime.now() + timedelta(days=1),
                    purpose='Regular health checkup',
                    status='scheduled'
                ),
                Appointment(
                    senior_id=senior2.id,
                    nurse_id=nurse2.id,
                    appointment_date=datetime.now() + timedelta(days=2),
                    purpose='Blood pressure monitoring',
                    status='scheduled'
                ),
                Appointment(
                    senior_id=senior1.id,
                    nurse_id=nurse1.id,
                    appointment_date=datetime.now() - timedelta(days=5),
                    purpose='Follow-up visit',
                    status='completed'
                )
            ]
            
            db.session.add_all(appointments)
            db.session.commit()
            print("✅ Appointments created successfully")
            
            # ========== CREATE HEALTH RECORDS ==========
            print("🏥 Creating sample health records...")
            
            health_records = [
                HealthRecord(
                    senior_id=senior1.id,
                    recorded_by=nurse1.id,
                    blood_pressure_systolic=120,
                    blood_pressure_diastolic=80,
                    blood_sugar=5.5,
                    oxygen_level=98.0,
                    body_temperature=36.8,
                    weight=70.5,
                    heart_rate=72,
                    notes='All vitals normal, patient feeling well'
                ),
                HealthRecord(
                    senior_id=senior2.id,
                    recorded_by=nurse2.id,
                    blood_pressure_systolic=135,
                    blood_pressure_diastolic=85,
                    blood_sugar=6.2,
                    oxygen_level=96.5,
                    body_temperature=37.1,
                    weight=65.2,
                    heart_rate=68,
                    notes='Slightly elevated blood pressure, advised to monitor'
                ),
                HealthRecord(
                    senior_id=senior1.id,
                    recorded_by=nurse1.id,
                    blood_pressure_systolic=118,
                    blood_pressure_diastolic=78,
                    blood_sugar=5.8,
                    oxygen_level=97.8,
                    body_temperature=36.9,
                    weight=70.2,
                    heart_rate=75,
                    notes='Follow-up check, improvements noted'
                )
            ]
            
            db.session.add_all(health_records)
            db.session.commit()
            print("✅ Health records created successfully")
            
            # ========== CREATE EMERGENCY CONTACTS ==========
            print("🆘 Creating sample emergency contacts...")
            
            emergency_contacts = [
                EmergencyContact(
                    senior_id=senior1.id,
                    name='Jane Smith',
                    relationship='Daughter',
                    phone='+1-778-123-4567',
                    email='jane.smith@email.com',
                    priority=1
                ),
                EmergencyContact(
                    senior_id=senior1.id,
                    name='Dr. Robert Chen',
                    relationship='Family Doctor',
                    phone='+1-604-987-6543',
                    email='r.chen@clinic.com',
                    priority=2
                ),
                EmergencyContact(
                    senior_id=senior2.id,
                    name='David Johnson',
                    relationship='Son',
                    phone='+1-778-555-1122',
                    email='david.johnson@email.com',
                    priority=1
                )
            ]
            
            db.session.add_all(emergency_contacts)
            db.session.commit()
            print("✅ Emergency contacts created successfully")
            
            # ========== CREATE MEDICATIONS ==========
            print("💊 Creating sample medications...")
            
            medications = [
                Medication(
                    senior_id=senior1.id,
                    name='Lisinopril',
                    dosage='10mg',
                    frequency='once daily',
                    time_of_day='morning',
                    instructions='Take with food, monitor blood pressure'
                ),
                Medication(
                    senior_id=senior1.id,
                    name='Metformin',
                    dosage='500mg',
                    frequency='twice daily',
                    time_of_day='morning and evening',
                    instructions='Take with meals'
                ),
                Medication(
                    senior_id=senior2.id,
                    name='Atorvastatin',
                    dosage='20mg',
                    frequency='once daily',
                    time_of_day='evening',
                    instructions='Take at bedtime'
                )
            ]
            
            db.session.add_all(medications)
            db.session.commit()
            print("✅ Medications created successfully")
            
            # ========== CREATE COMMUNITY EVENTS ==========
            print("👥 Creating sample community events...")
            
            community_events = [
                CommunityEvent(
                    title='Morning Yoga for Seniors',
                    description='Gentle yoga session with certified instructor. Suitable for all fitness levels.',
                    event_date=datetime.now() + timedelta(days=3),
                    location='Community Hall',
                    event_type='exercise',
                    created_by=nurse1.id,
                    max_participants=15
                ),
                CommunityEvent(
                    title='Healthy Eating Workshop',
                    description='Learn about nutrition and healthy meal planning for seniors.',
                    event_date=datetime.now() + timedelta(days=7),
                    location='Dining Room',
                    event_type='educational',
                    created_by=nurse2.id,
                    max_participants=20
                ),
                CommunityEvent(
                    title='Social Tea & Games',
                    description='Relaxed social gathering with tea, coffee, and board games.',
                    event_date=datetime.now() + timedelta(days=5),
                    location='Common Room',
                    event_type='social',
                    created_by=nurse1.id,
                    max_participants=25
                )
            ]
            
            db.session.add_all(community_events)
            db.session.commit()
            print("✅ Community events created successfully")
            
            # ========== FINAL SUMMARY ==========
            print("\n" + "="*50)
            print("🎉 SAMPLE DATA CREATION COMPLETE!")
            print("="*50)
            print("\n📊 DATABASE SUMMARY:")
            print(f"👥 Users: {User.query.count()} (3 seniors, 2 nurses)")
            print(f"📅 Appointments: {Appointment.query.count()}")
            print(f"🏥 Health Records: {HealthRecord.query.count()}")
            print(f"🆘 Emergency Contacts: {EmergencyContact.query.count()}")
            print(f"💊 Medications: {Medication.query.count()}")
            print(f"👥 Community Events: {CommunityEvent.query.count()}")
            
            print("\n🔑 TEST LOGIN CREDENTIALS:")
            print("SENIORS:")
            print("  john.senior@silvercare.com / password123")
            print("  mary.senior@silvercare.com / password123")
            print("  robert.senior@silvercare.com / password123")
            print("\nNURSES:")
            print("  sarah.nurse@silvercare.com / password123")
            print("  mike.nurse@silvercare.com / password123")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating sample data: {e}")
            raise