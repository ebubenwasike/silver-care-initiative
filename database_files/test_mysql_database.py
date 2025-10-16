from database.models import User, Appointment, HealthRecord, EmergencyContact, Medication, CommunityEvent
from datetime import datetime, timedelta

class MySQLQueries:
    """Practical MySQL queries for the application"""
    
    @staticmethod
    def get_senior_dashboard_data(senior_id):
        """Get all data needed for senior dashboard"""
        return {
            'user': User.query.get(senior_id),
            'upcoming_appointments': Appointment.query.filter_by(
                senior_id=senior_id, 
                status='scheduled'
            ).order_by(Appointment.appointment_date.asc()).limit(5).all(),
            'recent_health': HealthRecord.query.filter_by(
                senior_id=senior_id
            ).order_by(HealthRecord.date_recorded.desc()).limit(3).all(),
            'emergency_contacts': EmergencyContact.query.filter_by(
                senior_id=senior_id, 
                is_active=True
            ).order_by(EmergencyContact.priority).all(),
            'current_medications': Medication.query.filter_by(
                senior_id=senior_id, 
                is_active=True
            ).all(),
            'upcoming_events': CommunityEvent.query.filter(
                CommunityEvent.event_date >= datetime.now(),
                CommunityEvent.is_active == True
            ).order_by(CommunityEvent.event_date.asc()).limit(5).all()
        }
    
    @staticmethod
    def get_nurse_dashboard_data(nurse_id):
        """Get all data needed for nurse dashboard"""
        return {
            'user': User.query.get(nurse_id),
            'today_appointments': Appointment.query.filter(
                Appointment.nurse_id == nurse_id,
                Appointment.appointment_date >= datetime.now().date(),
                Appointment.appointment_date < datetime.now().date() + timedelta(days=1)
            ).all(),
            'assigned_seniors': User.query.filter_by(role='senior').all(),
            'recent_health_updates': HealthRecord.query.filter(
                HealthRecord.recorded_by == nurse_id
            ).order_by(HealthRecord.date_recorded.desc()).limit(10).all()
        }
    
    @staticmethod
    def get_health_trends(senior_id, days=30):
        """Get health data trends for a senior"""
        start_date = datetime.now() - timedelta(days=days)
        
        return HealthRecord.query.filter(
            HealthRecord.senior_id == senior_id,
            HealthRecord.date_recorded >= start_date
        ).order_by(HealthRecord.date_recorded.asc()).all()
    
    @staticmethod
    def get_available_time_slots(nurse_id, date):
        """Get available appointment slots for a nurse on specific date"""
        # Get existing appointments for that day
        existing_appointments = Appointment.query.filter(
            Appointment.nurse_id == nurse_id,
            Appointment.appointment_date >= date,
            Appointment.appointment_date < date + timedelta(days=1),
            Appointment.status == 'scheduled'
        ).all()
        
        # Generate available slots (example logic)
        available_slots = []
        start_time = datetime.combine(date, datetime.strptime('09:00', '%H:%M').time())
        
        for i in range(8):  # 8 slots from 9 AM to 5 PM
            slot_time = start_time + timedelta(hours=i)
            # Check if slot is not booked
            if not any(apt.appointment_date.hour == slot_time.hour for apt in existing_appointments):
                available_slots.append(slot_time)
        
        return available_slots
    
    @staticmethod
    def search_seniors(search_term):
        """Search seniors by name or email"""
        return User.query.filter(
            User.role == 'senior',
            (User.first_name.ilike(f'%{search_term}%')) | 
            (User.last_name.ilike(f'%{search_term}%')) |
            (User.email.ilike(f'%{search_term}%'))
        ).all()