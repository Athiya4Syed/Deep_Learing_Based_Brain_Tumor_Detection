#!/usr/bin/env python3
"""
Test script to verify PDF generation is working
"""

import os
import sys
from pdf_generator import generate_pdf_report

def test_pdf_generation():
    """Test PDF generation with sample data"""
    
    # Sample patient info
    patient_info = {
        'name': 'Test User',
        'age': 35,
        'gender': 'Male',
        'contact': '+1234567890',
        'email': 'test@example.com'
    }
    
    # Sample result data
    result_data = {
        'name': 'Pituitary Tumor',
        'predicted_stage': 'II',
        'confidence': 85.5,
        'description': 'A tumor that forms in the pituitary gland, a small gland at the base of the brain.',
        'cell_structure': 'Pituitary tumors typically show uniform, small round cells with regular nuclei.',
        'symptoms': ['Headaches', 'Vision problems', 'Hormonal imbalances'],
        'treatments': ['Surgical removal', 'Radiation therapy', 'Medication'],
        'prevention': ['Regular medical check-ups', 'Monitor hormone levels'],
        'severity': 'Moderate',
        'survival_rate': '85-95% with proper treatment',
        'stage_info': {
            'description': 'Macroadenoma (10-30mm)',
            'characteristics': 'Larger tumor with moderate symptoms',
            'treatment_approach': 'Surgical removal recommended',
            'prognosis': 'Very good - 90% survival rate'
        },
        'image_features': {
            'image_size': '512x512 pixels',
            'mean_intensity': 45.2,
            'edge_density': 6.5,
            'contour_count': 150,
            'texture_variance': 8500.0
        },
        'analysis_date': '2025-09-21 16:45:00'
    }
    
    # Use an existing image file for testing
    image_path = "./uploads/Te-gl_0015.jpg"
    
    if not os.path.exists(image_path):
        print(f"❌ Test image not found: {image_path}")
        print("Please ensure there's an image in the uploads folder")
        return False
    
    print("🧪 Testing PDF generation...")
    print(f"Patient: {patient_info['name']}")
    print(f"Image: {image_path}")
    print(f"Image exists: {os.path.exists(image_path)}")
    
    try:
        # Generate PDF
        pdf_path = generate_pdf_report(
            patient_info,
            result_data,
            image_path,
            "reports"
        )
        
        print(f"📄 PDF generated at: {pdf_path}")
        
        # Check if PDF was created
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"✅ PDF created successfully!")
            print(f"📊 File size: {file_size} bytes")
            print(f"📁 Location: {pdf_path}")
            return True
        else:
            print(f"❌ PDF was not created at {pdf_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error during PDF generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_generation()
    if success:
        print("\n🎉 PDF generation test PASSED!")
    else:
        print("\n💥 PDF generation test FAILED!")
        sys.exit(1)

