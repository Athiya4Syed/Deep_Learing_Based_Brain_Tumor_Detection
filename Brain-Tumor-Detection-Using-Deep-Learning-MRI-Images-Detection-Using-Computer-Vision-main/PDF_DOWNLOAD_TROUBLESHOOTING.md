# PDF Download Troubleshooting Guide

## Issue: PDF Download Not Working in Doctor's Interface

### Step 1: Check the Current Status

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Visit the debug page**:
   ```
   http://localhost:5000/debug
   ```

3. **Check PDF status**:
   ```
   http://localhost:5000/check_pdf_status
   ```

### Step 2: Test the Download Functionality

1. **Go to doctor's interface**:
   ```
   http://localhost:5000/doctor
   ```

2. **For each report, click "Test Download"** to see detailed information about:
   - PDF path in database
   - File existence
   - File path details

3. **Check the console output** for detailed debugging information

### Step 3: Common Issues and Solutions

#### Issue 1: "PDF not found for this report"
**Cause**: The PDF path is empty or null in the database
**Solution**: 
- Click "Generate Updated PDF" to create a new PDF
- Check if the original analysis completed successfully

#### Issue 2: "PDF file not found and could not be regenerated"
**Cause**: The PDF file was deleted or never created
**Solution**:
- Click "Generate Updated PDF" to regenerate the PDF
- Check the console for PDF generation errors

#### Issue 2.1: "tuple index out of range" error during PDF regeneration
**Cause**: Database column indices mismatch in the regeneration function
**Solution**:
- The function has been updated to handle variable column counts safely
- Check the console output for detailed column information
- Use the debug route `/debug_report/<id>` to see the exact database structure
- If the error persists, check the database schema matches the expected structure

#### Issue 3: "Database connection failed"
**Cause**: Database connection issues
**Solution**:
- Ensure PostgreSQL is running
- Check database credentials in `database.py`
- Restart the application

#### Issue 4: "File not found" error
**Cause**: File path issues
**Solution**:
- Check if the reports directory exists
- Verify file permissions
- Check the console output for file path details

### Step 4: Manual Testing

1. **Test a specific report**:
   ```
   http://localhost:5000/test_download/1
   ```
   (Replace "1" with the actual report ID)

2. **Check available PDFs**:
   ```
   http://localhost:5000/list_pdfs
   ```

3. **Test direct download**:
   ```
   http://localhost:5000/download_report_pdf/1
   ```
   (Replace "1" with the actual report ID)

### Step 5: Console Debugging

Look for these messages in the console:

```
=== Download request for report ID: X ===
Database result: (path_to_pdf,)
PDF path from DB: /path/to/reports/filename.pdf
Extracted filename: filename.pdf
File exists: True/False
```

### Step 6: File System Check

1. **Check reports directory**:
   ```bash
   ls -la reports/
   ```

2. **Check file permissions**:
   ```bash
   ls -la reports/*.pdf
   ```

3. **Check current working directory**:
   ```bash
   pwd
   ```

### Step 7: Database Check

1. **Connect to PostgreSQL**:
   ```bash
   psql -U postgres -d BrainTumor
   ```

2. **Check reports table**:
   ```sql
   SELECT id, pdf_path FROM reports;
   ```

3. **Check specific report**:
   ```sql
   SELECT * FROM reports WHERE id = 1;
   ```

### Step 8: Regeneration Process

If PDFs are missing:

1. **Click "Generate Updated PDF"** in the doctor's interface
2. **Check console output** for generation errors
3. **Verify the new PDF was created** in the reports directory
4. **Try downloading again**

### Step 8.1: Debug PDF Generation (Advanced)

If regeneration is failing, use the debug script:

1. **Run the debug script**:
   ```bash
   python debug_pdf_issue.py
   ```
   This will list all reports in the database.

2. **Debug a specific report**:
   ```bash
   python debug_pdf_issue.py <report_id>
   ```
   Replace `<report_id>` with the actual report ID.

3. **Check the output** for:
   - Database connection issues
   - Missing image files
   - PDF generation errors
   - File permission issues

### Step 8.2: Common PDF Generation Issues

#### Issue: "Image file not found"
**Cause**: The uploaded image was moved or deleted
**Solution**: 
- Check if the image exists in the uploads directory
- The debug script will try to find the image automatically
- If the image is missing, you may need to re-upload it

#### Issue: "Reports directory not found"
**Cause**: The reports directory was deleted
**Solution**: 
- The system will automatically create the reports directory
- Check file permissions on the project directory

#### Issue: "Database column index error"
**Cause**: Database structure mismatch
**Solution**: 
- The debug script will show the correct column indices
- Check if the database schema matches the expected structure

#### Issue: "PDF generation failed"
**Cause**: Missing dependencies or file permission issues
**Solution**: 
- Ensure ReportLab is installed: `pip install reportlab`
- Check file permissions on the project directory
- Verify that the image file is a valid image format

### Step 9: Final Verification

1. **Upload a new image** and complete analysis
2. **Go to doctor's interface** and test download
3. **Add doctor's notes** and regenerate PDF
4. **Test download again**

### Common Error Messages and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "PDF not found for this report" | Empty PDF path in DB | Generate new PDF |
| "PDF file not found" | File deleted/missing | Regenerate PDF |
| "Database connection failed" | DB not running | Start PostgreSQL |
| "File not found" | Path issues | Check file paths |
| "Permission denied" | File permissions | Fix permissions |

### Debug Routes Available

- `/debug` - Main debug page
- `/check_pdf_status` - PDF status check
- `/list_pdfs` - List available PDFs
- `/test_download/<id>` - Test specific report
- `/download_report_pdf/<id>` - Download specific report
- `/debug_report/<id>` - Debug database structure for specific report

### Support

If issues persist:

1. Check console output for detailed error messages
2. Use the debug routes to gather information
3. Verify database connectivity
4. Check file system permissions
5. Ensure all dependencies are installed
