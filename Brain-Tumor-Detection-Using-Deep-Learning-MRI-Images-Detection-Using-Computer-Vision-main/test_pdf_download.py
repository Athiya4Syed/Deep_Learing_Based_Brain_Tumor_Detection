#!/usr/bin/env python3
"""
Test script to verify PDF download functionality
"""

import os
import requests
import json

def test_pdf_download():
    """Test the PDF download functionality"""
    
    # Base URL for the Flask app
    base_url = "http://localhost:5000"
    
    print("Testing PDF Download Functionality")
    print("=" * 50)
    
    # Test 1: Check PDF status
    print("\n1. Checking PDF status...")
    try:
        response = requests.get(f"{base_url}/check_pdf_status")
        if response.status_code == 200:
            status = response.json()
            print(f"Current directory: {status['current_dir']}")
            print(f"Reports directory: {status['reports_dir']}")
            print(f"Reports directory exists: {status['reports_dir_exists']}")
            print(f"Files in reports directory: {len(status['files'])}")
            for file in status['files']:
                print(f"  - {file['name']} ({file['size']} bytes)")
        else:
            print(f"Error checking status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: List PDFs
    print("\n2. Listing PDF files...")
    try:
        response = requests.get(f"{base_url}/list_pdfs")
        if response.status_code == 200:
            data = response.json()
            print(f"PDF files: {data.get('pdf_files', [])}")
        else:
            print(f"Error listing PDFs: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Try to download existing PDF
    print("\n3. Testing PDF download...")
    try:
        response = requests.get(f"{base_url}/test_pdf_download")
        if response.status_code == 200:
            print("PDF download successful!")
            print(f"Content length: {len(response.content)} bytes")
        else:
            print(f"PDF download failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_pdf_download()
