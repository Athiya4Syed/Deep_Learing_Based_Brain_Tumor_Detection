import psycopg2
from psycopg2 import Error
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'BrainTumor',
            'user': 'postgres',
            'password': 'Suhas1208',
            'port': '5432'
        }
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(**self.db_config)
            self.cursor = self.connection.cursor()
            print("✅ Successfully connected to PostgreSQL database")
            return True
        except Error as e:
            print(f"❌ Error connecting to PostgreSQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("✅ Database connection closed")
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            # Create patients table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INTEGER NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    contact VARCHAR(20) NOT NULL,
                    email VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create reports table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id SERIAL PRIMARY KEY,
                    patient_id INTEGER REFERENCES patients(id),
                    image_path VARCHAR(255) NOT NULL,
                    pdf_path VARCHAR(255) NOT NULL,
                    tumor_type VARCHAR(50),
                    tumor_stage VARCHAR(10),
                    confidence_score DECIMAL(5,2),
                    prediction_result VARCHAR(20) NOT NULL,
                    image_features JSONB,
                    doctor_notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.connection.commit()
            print("✅ Database tables created successfully")
            return True
            
        except Error as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    def insert_patient(self, name, age, gender, contact, email):
        """Insert patient information"""
        try:
            self.cursor.execute("""
                INSERT INTO patients (name, age, gender, contact, email)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (name, age, gender, contact, email))
            
            patient_id = self.cursor.fetchone()[0]
            self.connection.commit()
            print(f"✅ Patient inserted with ID: {patient_id}")
            return patient_id
            
        except Error as e:
            print(f"❌ Error inserting patient: {e}")
            return None
    
    def insert_report(self, patient_id, image_path, pdf_path, tumor_type, tumor_stage, 
                     confidence_score, prediction_result, image_features, doctor_notes=""):
        """Insert report information"""
        try:
            self.cursor.execute("""
                INSERT INTO reports (patient_id, image_path, pdf_path, tumor_type, 
                                   tumor_stage, confidence_score, prediction_result, 
                                   image_features, doctor_notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (patient_id, image_path, pdf_path, tumor_type, tumor_stage,
                  confidence_score, prediction_result, image_features, doctor_notes))
            
            report_id = self.cursor.fetchone()[0]
            self.connection.commit()
            print(f"✅ Report inserted with ID: {report_id}")
            return report_id
            
        except Error as e:
            print(f"❌ Error inserting report: {e}")
            return None
    
    def get_patient_reports(self, patient_id):
        """Get all reports for a specific patient"""
        try:
            self.cursor.execute("""
                SELECT r.*, p.name, p.age, p.gender, p.contact, p.email
                FROM reports r
                JOIN patients p ON r.patient_id = p.id
                WHERE r.patient_id = %s
                ORDER BY r.created_at DESC
            """, (patient_id,))
            
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"❌ Error fetching patient reports: {e}")
            return []
    
    def get_all_reports(self):
        """Get all reports with patient information"""
        try:
            self.cursor.execute("""
                SELECT r.*, p.name, p.age, p.gender, p.contact, p.email
                FROM reports r
                JOIN patients p ON r.patient_id = p.id
                ORDER BY r.created_at DESC
            """)
            
            return self.cursor.fetchall()
            
        except Error as e:
            print(f"❌ Error fetching all reports: {e}")
            return []
    
    def update_doctor_notes(self, report_id, notes):
        """Update doctor's notes for a specific report"""
        try:
            self.cursor.execute("""
                UPDATE reports 
                SET doctor_notes = %s 
                WHERE id = %s
            """, (notes, report_id))
            
            self.connection.commit()
            print(f"✅ Doctor's notes updated for report ID: {report_id}")
            return True
            
        except Error as e:
            print(f"❌ Error updating doctor's notes: {e}")
            return False

# Initialize database
def init_database():
    """Initialize database connection and create tables"""
    db = DatabaseManager()
    if db.connect():
        db.create_tables()
        db.disconnect()
        return True
    return False

if __name__ == "__main__":
    init_database()
