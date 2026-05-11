#!/usr/bin/env python3
"""
Test script to verify the PDF download fix
"""

import os
import sys

def test_pdf_paths():
    """Test PDF path handling"""
    print("Testing PDF Path Handling")
    print("=" * 40)
    
    # Test cases
    test_paths = [
        "reports/BrainTumor_Report_John_20241201_120000.pdf",
        "BrainTumor_Report_John_20241201_120000.pdf",
        "/full/path/to/reports/BrainTumor_Report_John_20241201_120000.pdf",
        "",
        None
    ]
    
    for path in test_paths:
        if path:
            filename = os.path.basename(path) if '/' in path else path
            print(f"Path: {path}")
            print(f"  Filename: {filename}")
            print(f"  Has slash: {'/' in path}")
        else:
            print(f"Path: {path}")
            print(f"  Filename: None")
            print(f"  Has slash: False")
        print()

def test_template_logic():
    """Test the template logic for PDF paths"""
    print("Testing Template Logic")
    print("=" * 40)
    
    # Simulate the template logic
    test_reports = [
        ("reports/BrainTumor_Report_John_20241201_120000.pdf", 1),
        ("BrainTumor_Report_John_20241201_120000.pdf", 2),
        ("", 3),
        (None, 4)
    ]
    
    for pdf_path, report_id in test_reports:
        print(f"Report ID: {report_id}")
        print(f"PDF Path: {pdf_path}")
        
        if pdf_path:
            # Simulate the template logic
            filename = pdf_path.split('/')[-1] if '/' in pdf_path else pdf_path
            download_url = f"/download_report_pdf/{report_id}"
            print(f"  Filename: {filename}")
            print(f"  Download URL: {download_url}")
        else:
            print(f"  No PDF path available")
        print()

def check_reports_directory():
    """Check the reports directory"""
    print("Checking Reports Directory")
    print("=" * 40)
    
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        files = os.listdir(reports_dir)
        pdf_files = [f for f in files if f.endswith('.pdf')]
        print(f"Reports directory exists: {os.path.exists(reports_dir)}")
        print(f"Total files: {len(files)}")
        print(f"PDF files: {len(pdf_files)}")
        for pdf in pdf_files:
            file_path = os.path.join(reports_dir, pdf)
            size = os.path.getsize(file_path)
            print(f"  - {pdf} ({size} bytes)")
    else:
        print(f"Reports directory does not exist")
        print(f"Current directory: {os.getcwd()}")

if __name__ == "__main__":
    test_pdf_paths()
    test_template_logic()
    check_reports_directory()
