# PDF Download Debug Guide

This guide helps you troubleshoot PDF download issues in the Brain Tumor Detection application.

## Quick Debug Steps

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Visit the debug page**:
   ```
   http://localhost:5000/debug
   ```

3. **Check PDF status**:
   - The debug page will show you the current status of PDF files
   - It will list all available PDF files in the reports directory
   - You can test downloads directly from this page

## Debug Routes

The application now includes several debug routes to help troubleshoot PDF issues:

### `/debug`
- **Purpose**: Main debug page with visual interface
- **Usage**: Visit in browser to see PDF status and test downloads

### `/check_pdf_status`
- **Purpose**: Get detailed status of PDF files and directories
- **Usage**: Returns JSON with current directory, reports directory, and file information

### `/list_pdfs`
- **Purpose**: List all available PDF files
- **Usage**: Returns JSON with list of PDF files in reports directory

### `/test_pdf_download`
- **Purpose**: Test PDF download functionality
- **Usage**: Attempts to download the first available PDF file

## Common Issues and Solutions

### Issue: "File not found" error
**Symptoms**: Clicking download button shows "File not found" error

**Possible Causes**:
1. PDF file was not generated successfully
2. File path is incorrect
3. Reports directory doesn't exist

**Solutions**:
1. Check the debug page (`/debug`) to see if PDF files exist
2. Look at console output for PDF generation errors
3. Ensure the reports directory exists and is writable

### Issue: PDF generation fails
**Symptoms**: No PDF file is created after analysis

**Possible Causes**:
1. Missing dependencies (reportlab)
2. Image file not found
3. Permission issues

**Solutions**:
1. Install required dependencies: `pip install reportlab`
2. Check that uploaded images are accessible
3. Ensure write permissions to reports directory

### Issue: Download button not visible
**Symptoms**: No download button appears on results page

**Possible Causes**:
1. PDF generation failed silently
2. `result_data['pdf_path']` is not set

**Solutions**:
1. Check console output for PDF generation errors
2. Verify that `result_data['pdf_path']` is set correctly
3. Use debug page to check PDF status

## Testing the Fix

1. **Upload an image** through the main interface
2. **Complete the analysis** process
3. **Check the debug page** (`/debug`) to verify PDF was created
4. **Try downloading** the PDF from the results page
5. **If issues persist**, check the console output for error messages

## Console Debugging

The application now includes extensive console logging. Look for these messages:

```
PDF generated successfully at: /path/to/reports/filename.pdf
PDF filename: filename.pdf
PDF exists: True
```

If you see errors like:
```
Error generating PDF: [error message]
ERROR: PDF was not created at [path]
```

This indicates the PDF generation failed and needs to be investigated.

## Manual Testing

You can also test the PDF download manually:

1. **Check available PDFs**:
   ```
   http://localhost:5000/list_pdfs
   ```

2. **Test download**:
   ```
   http://localhost:5000/test_pdf_download
   ```

3. **Check status**:
   ```
   http://localhost:5000/check_pdf_status
   ```

## File Structure

The application expects this file structure:
```
your_project/
├── main.py
├── pdf_generator.py
├── reports/          # PDF files are stored here
│   └── *.pdf
├── uploads/          # Uploaded images are stored here
│   └── *.jpg
└── templates/
    ├── result.html
    └── debug.html
```

## Dependencies

Make sure you have these Python packages installed:
```bash
pip install flask tensorflow keras opencv-python reportlab
```

## Support

If you continue to experience issues:

1. Check the console output for error messages
2. Use the debug page to verify file status
3. Ensure all dependencies are installed
4. Check file permissions on the reports directory
