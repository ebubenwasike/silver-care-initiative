from database.models import db, User, Appointment, HealthRecord
from datetime import datetime

def create_sample_data(app):
    with app.app_context():
        if not User.query.first():  # Only seed if empty
            try:
                user1 = User(username='Priya', email='priya@example.com', password='12345')
                user2 = User(username='Arun', email='arun@example.com', password='12345')

                db.session.add_all([user1, user2])
                db.session.commit()

                appt1 = Appointment(user_id=user1.id, date=datetime(2025, 10, 20), description="Doctor checkup")
                record1 = HealthRecord(user_id=user1.id, condition="Healthy", doctor="Dr. Mehta")

                db.session.add_all([appt1, record1])
                db.session.commit()

                print("🎉 SAMPLE DATA CREATION COMPLETE!")
            except Exception as e:
                print(f"❌ Error seeding data: {e}")
