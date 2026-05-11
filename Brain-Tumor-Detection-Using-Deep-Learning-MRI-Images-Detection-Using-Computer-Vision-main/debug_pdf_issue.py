#!/usr/bin/env python3
"""
Debug script to identify PDF generation issues
"""

import os
import sys
from database import DatabaseManager
from pdf_generator import generate_pdf_report

def debug_pdf_generation(report_id):
    """Debug PDF generation for a specific report"""
    print(f"=== Debugging PDF Generation for Report ID: {report_id} ===")
    
    db_manager = DatabaseManager()
    
    if db_manager.connect():
        try:
            # Get the specific report
            db_manager.cursor.execute("""
                SELECT r.*, p.name, p.age, p.gender, p.contact, p.email
                FROM reports r
                JOIN patients p ON r.patient_id = p.id
                WHERE r.id = %s
            """, (report_id,))
            
            report = db_manager.cursor.fetchone()
            if not report:
                print(f"❌ Report not found for ID: {report_id}")
                return
            
            print(f"✅ Report found: {report}")
            
            # Check database structure
            print("\n=== Database Structure ===")
            print(f"Report columns: {len(report)}")
            print("Expected structure:")
            print("r.id, r.patient_id, r.image_path, r.pdf_path, r.tumor_type, r.tumor_stage, r.confidence_score, r.prediction_result, r.image_features, r.doctor_notes, r.created_at, p.name, p.age, p.gender, p.contact, p.email")
            
            # Prepare patient info
            patient_info = {
                'name': report[12],  # p.name
                'age': report[13],   # p.age
                'gender': report[14], # p.gender
                'contact': report[15], # p.contact
                'email': report[16]   # p.email
            }
            
            print(f"\n✅ Patient info: {patient_info}")
            
            # Prepare result data
            result_data = {
                'name': report[3] if report[3] else 'No Tumor Detected',  # r.tumor_type
                'predicted_stage': report[4] if report[4] else 'N/A',     # r.tumor_stage
                'confidence': report[5] if report[5] else 0,              # r.confidence_score
                'description': 'Brain tumor analysis report',
                'severity': 'Moderate' if report[3] and report[3] != 'No Tumor Detected' else 'None',
                'survival_rate': '85-95% with proper treatment' if report[3] and report[3] != 'No Tumor Detected' else 'N/A'
            }
            
            print(f"✅ Result data: {result_data}")
            
            # Get doctor's notes
            doctor_notes = report[9] if report[9] else ""  # r.doctor_notes
            print(f"✅ Doctor notes: {doctor_notes}")
            
            # Get image path
            image_path = report[2]  # r.image_path
            print(f"✅ Image path: {image_path}")
            
            # Check if image exists
            print(f"\n=== Image File Check ===")
            print(f"Image path: {image_path}")
            print(f"Image exists: {os.path.exists(image_path)}")
            
            if not os.path.exists(image_path):
                print(f"❌ Image file not found at {image_path}")
                # Try to find the image in uploads directory
                uploads_dir = os.path.join(os.getcwd(), 'uploads')
                image_filename = os.path.basename(image_path)
                alt_image_path = os.path.join(uploads_dir, image_filename)
                print(f"Trying alternative path: {alt_image_path}")
                print(f"Alternative path exists: {os.path.exists(alt_image_path)}")
                
                if os.path.exists(alt_image_path):
                    image_path = alt_image_path
                    print(f"✅ Found image at alternative path: {image_path}")
                else:
                    print(f"❌ Image not found at alternative path either: {alt_image_path}")
                    # List files in uploads directory
                    if os.path.exists(uploads_dir):
                        print(f"Files in uploads directory:")
                        for file in os.listdir(uploads_dir):
                            print(f"  - {file}")
                    else:
                        print(f"Uploads directory does not exist: {uploads_dir}")
                    return
            
            # Check reports directory
            print(f"\n=== Reports Directory Check ===")
            reports_dir = "reports"
            print(f"Reports directory: {reports_dir}")
            print(f"Reports directory exists: {os.path.exists(reports_dir)}")
            
            if not os.path.exists(reports_dir):
                print(f"Creating reports directory...")
                os.makedirs(reports_dir)
                print(f"Reports directory created: {os.path.exists(reports_dir)}")
            
            # List existing PDFs
            if os.path.exists(reports_dir):
                pdf_files = [f for f in os.listdir(reports_dir) if f.endswith('.pdf')]
                print(f"Existing PDF files: {pdf_files}")
            
            # Try to generate PDF
            print(f"\n=== PDF Generation Test ===")
            try:
                print("Calling generate_pdf_report...")
                new_pdf_path = generate_pdf_report(
                    patient_info, 
                    result_data, 
                    image_path,
                    "reports",
                    doctor_notes
                )
                
                print(f"✅ Generated PDF path: {new_pdf_path}")
                print(f"✅ PDF file exists: {os.path.exists(new_pdf_path)}")
                
                if os.path.exists(new_pdf_path):
                    print(f"✅ PDF file size: {os.path.getsize(new_pdf_path)} bytes")
                    
                    # Update database
                    db_manager.cursor.execute("""
                        UPDATE reports 
                        SET pdf_path = %s 
                        WHERE id = %s
                    """, (new_pdf_path, report_id))
                    
                    db_manager.connection.commit()
                    print(f"✅ Database updated with new PDF path")
                    
                    return new_pdf_path
                else:
                    print(f"❌ PDF file was not created")
                    return None
                
            except Exception as e:
                print(f"❌ Error generating PDF: {e}")
                import traceback
                traceback.print_exc()
                return None
                
        except Exception as e:
            print(f"❌ Error in debug function: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db_manager.disconnect()
    else:
        print("❌ Failed to connect to database")

def list_all_reports():
    """List all reports in the database"""
    print("=== All Reports in Database ===")
    
    db_manager = DatabaseManager()
    
    if db_manager.connect():
        try:
            reports = db_manager.get_all_reports()
            print(f"Total reports: {len(reports)}")
            
            for report in reports:
                print(f"Report ID: {report[0]}, Patient: {report[12]}, PDF: {report[3]}")
                
        finally:
            db_manager.disconnect()
    else:
        print("❌ Failed to connect to database")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        report_id = int(sys.argv[1])
        debug_pdf_generation(report_id)
    else:
        print("Usage: python debug_pdf_issue.py <report_id>")
        print("Or run without arguments to list all reports:")
        list_all_reports()
