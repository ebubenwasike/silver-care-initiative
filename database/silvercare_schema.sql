CREATE DATABASE IF NOT EXISTS silver_care_db;
USE silver_care_db;

-- STAFF TABLE
DROP TABLE IF EXISTS staff;
CREATE TABLE staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    security_question VARCHAR(255),
    security_answer VARCHAR(255),
    totp_secret VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INSERT YOUR WORKING STAFF ACCOUNT
INSERT INTO staff (email, password, first_name, last_name, totp_secret)
VALUES (
    'ebube@silvercare.org',
    'password123',   -- plain text matching your app.py
    'Ebube',
    'Nwasike',
    '5JJ4Y2AFGAZYGEIBX7G4EBXZVGADMF2O'
);

-- PATIENTS TABLE
DROP TABLE IF EXISTS patients;
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    dob DATE,
    phn VARCHAR(50) UNIQUE NOT NULL,
    emergency_contact VARCHAR(255),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES staff(id)
);

-- APPOINTMENTS TABLE
DROP TABLE IF EXISTS appointments;
CREATE TABLE appointments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    staff_id INT NOT NULL,
    appointment_date DATE NOT NULL,
    appointment_time VARCHAR(10) NOT NULL,
    appointment_type VARCHAR(100) NOT NULL,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

-- VITALS TABLE
DROP TABLE IF EXISTS vitals;
CREATE TABLE vitals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    blood_pressure VARCHAR(20),
    bmi DECIMAL(4,1),
    weight DECIMAL(5,1),
    height DECIMAL(5,1),
    respiratory_rate INT,
    temperature DECIMAL(4,1),
    heart_rate INT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
