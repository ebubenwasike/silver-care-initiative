# SilverCare Initiative 

<img width="1440" height="900" alt="Screenshot 2025-11-30 at 11 17 40 PM" src="https://github.com/user-attachments/assets/0a4e7402-6127-4b5e-abb3-9f3cdb71474d" />

SilverCare Portal is a web-based healthcare management system designed for senior homes. It provides staff and seniors with an easy, secure way to manage daily care activities such as appointments, vital signs, and personal information and prioritizes accesibility for elderly, non-tech-savvy people.

This project was built using Python (Flask) and MySQL, with a focus on clean UI, security, and real-world healthcare workflow features.

## Features

- **User Accounts** – Simple and secure sign-in system.
- **Appointment Booking** – Schedule and manage visits with healthcare providers.
- **Health Records Access** – View and track personal health information online.
- **Accessibility First** – Designed with ease-of-use in mind, specifically for seniors.

## Security
Hashed passwords,
Per-user TOTP secret for 2FA (staff only),
Security questions stored & encrypted,
Session based login control,
CSRF-safe fetch APIs,
No access to pages without authentication.

## How to Run Locally
1. Clone the repository: git clone https://github.com/ebubenwasike/silver-care-initiative.git
2. Navigate into the project: cd silver-care-initiative
3. Create a virtual environment: python3 -m venv venv
4. Activate it (Mac/Linux): source venv/bin/activate   (Windows: venv\Scripts\activate)
5. Install all dependencies: pip install -r requirements.txt
6. Start MySQL and create the database using the provided SQL script in /database (this sets up all tables and inserts the existing staff login).
7. Confirm the database silver_care_db exists and matches the configuration in app.py.
8. Run the Flask application: python3 app.py
9. Open the project in your browser at: http://127.0.0.1:5000
10. Log in using the pre-configured staff account included in the database script.
11. If any module errors appear, install missing packages using pip inside the virtual environment.
12. When finished, deactivate the environment using: deactivate

## Tech Stack
- **Frontend:** HTML, CSS, JS, Bootstrap 5
- **Backend:** Python Flask, MySQL Connector, pyotp (2FA), qrcode (QR generation)
- **Database:** MySQL
- **Deployment:** temporarily deployed using AWS EC2 instance and AWS RDS

### Members of this project:
Ebube Nwasike,
Mona Bakhshoodeh,
Su May Myo Paing,
Shubnoor Singh,
Priya.


Open-source — Free to modify and expand! <3
