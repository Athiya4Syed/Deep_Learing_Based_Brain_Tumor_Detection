#!/usr/bin/env python3
"""
Database Setup Script for Brain Tumor Detection System
This script initializes the PostgreSQL database and creates necessary tables.
"""

import psycopg2
from psycopg2 import Error
import sys

def setup_database():
    """Set up the database and create tables"""
    
    # Database configuration
    db_config = {
        'host': 'localhost',
        'database': 'BrainTumor',
        'user': 'postgres',
        'password': 'Suhas1208',
        'port': '5432'
    }
    
    try:
        # Connect to PostgreSQL
        print("🔌 Connecting to PostgreSQL database...")
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        print("✅ Successfully connected to PostgreSQL database")
        
        # Create patients table
        print("📋 Creating patients table...")
        cursor.execute("""
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
        print("✅ Patients table created successfully")
        
        # Create reports table
        print("📋 Creating reports table...")
        cursor.execute("""
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
        print("✅ Reports table created successfully")
        
        # Commit the changes
        connection.commit()
        print("✅ All changes committed successfully")
        
        # Verify tables exist
        print("🔍 Verifying tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('patients', 'reports')
        """)
        
        tables = cursor.fetchall()
        if len(tables) == 2:
            print("✅ All tables verified successfully")
            print("📊 Database setup completed!")
        else:
            print("❌ Some tables are missing")
            return False
            
    except Error as e:
        print(f"❌ Error during database setup: {e}")
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("✅ Database connection closed")
    
    return True

def test_database_connection():
    """Test database connection and basic operations"""
    
    db_config = {
        'host': 'localhost',
        'database': 'BrainTumor',
        'user': 'postgres',
        'password': 'Suhas1208',
        'port': '5432'
    }
    
    try:
        print("🧪 Testing database connection...")
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        
        # Test basic query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Database version: {version[0]}")
        
        # Test table queries
        cursor.execute("SELECT COUNT(*) FROM patients;")
        patient_count = cursor.fetchone()[0]
        print(f"✅ Patients table has {patient_count} records")
        
        cursor.execute("SELECT COUNT(*) FROM reports;")
        report_count = cursor.fetchone()[0]
        print(f"✅ Reports table has {report_count} records")
        
        cursor.close()
        connection.close()
        print("✅ Database test completed successfully")
        return True
        
    except Error as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Brain Tumor Detection Database Setup")
    print("=" * 50)
    
    # Setup database
    if setup_database():
        print("\n" + "=" * 50)
        print("🧪 Testing database setup...")
        test_database_connection()
    else:
        print("❌ Database setup failed!")
        sys.exit(1)
