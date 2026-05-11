from flask import Flask, render_template, request, send_from_directory, jsonify, redirect, url_for
from tensorflow.keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os
import cv2
from datetime import datetime
import json
from database import DatabaseManager
from pdf_generator import generate_pdf_report
from chatbot_service import medical_chatbot

# Initialize Flask app
app = Flask(__name__)

# Initialize database
db_manager = DatabaseManager()

# Initialize database tables
if db_manager.connect():
    db_manager.create_tables()
    db_manager.disconnect()
    print("✅ Database initialized successfully")

# Load the trained model
model = load_model('models/model.h5')

# Class labels
class_labels = ['pituitary', 'glioma', 'notumor', 'meningioma']

# Define the uploads folder
UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the reports folder
REPORTS_FOLDER = './reports'
if not os.path.exists(REPORTS_FOLDER):
    os.makedirs(REPORTS_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Tumor information database with staging information
tumor_info = {
    'pituitary': {
        'name': 'Pituitary Tumor',
        'description': 'A tumor that forms in the pituitary gland, a small gland at the base of the brain.',
        'cell_structure': 'Pituitary tumors typically show uniform, small round cells with regular nuclei and moderate cytoplasm. They often form solid sheets or trabecular patterns.',
        'symptoms': ['Headaches', 'Vision problems', 'Hormonal imbalances', 'Fatigue', 'Nausea'],
        'treatments': [
            'Surgical removal (transsphenoidal surgery)',
            'Radiation therapy',
            'Medication to control hormone levels',
            'Regular monitoring and follow-up'
        ],
        'prevention': [
            'Regular medical check-ups',
            'Monitor hormone levels',
            'Maintain healthy lifestyle',
            'Avoid exposure to radiation when possible'
        ],
        'severity': 'Moderate',
        'survival_rate': '85-95% with proper treatment',
        'stages': {
            'I': {
                'description': 'Microadenoma (< 10mm)',
                'characteristics': 'Small, well-defined tumor with minimal symptoms',
                'treatment_approach': 'Observation or medication therapy',
                'prognosis': 'Excellent - 95% survival rate'
            },
            'II': {
                'description': 'Macroadenoma (10-30mm)',
                'characteristics': 'Larger tumor with moderate symptoms',
                'treatment_approach': 'Surgical removal recommended',
                'prognosis': 'Very good - 90% survival rate'
            },
            'III': {
                'description': 'Large macroadenoma (30-40mm)',
                'characteristics': 'Large tumor with significant symptoms',
                'treatment_approach': 'Aggressive surgical treatment',
                'prognosis': 'Good - 85% survival rate'
            },
            'IV': {
                'description': 'Giant adenoma (> 40mm)',
                'characteristics': 'Very large tumor with severe symptoms',
                'treatment_approach': 'Complex surgical intervention required',
                'prognosis': 'Moderate - 75% survival rate'
            },
            'V': {
                'description': 'Invasive pituitary carcinoma',
                'characteristics': 'Malignant tumor with distant spread',
                'treatment_approach': 'Multimodal therapy including chemotherapy',
                'prognosis': 'Poor - 40% survival rate'
            }
        }
    },
    'glioma': {
        'name': 'Glioma',
        'description': 'A type of tumor that occurs in the brain and spinal cord, arising from glial cells.',
        'cell_structure': 'Gliomas show irregular, pleomorphic cells with hyperchromatic nuclei. They often infiltrate surrounding brain tissue and may show areas of necrosis.',
        'symptoms': ['Seizures', 'Headaches', 'Personality changes', 'Memory problems', 'Difficulty speaking'],
        'treatments': [
            'Surgical resection when possible',
            'Chemotherapy',
            'Radiation therapy',
            'Targeted therapy',
            'Clinical trials for advanced cases'
        ],
        'prevention': [
            'Avoid exposure to ionizing radiation',
            'Maintain healthy diet rich in antioxidants',
            'Regular exercise',
            'Avoid smoking and excessive alcohol'
        ],
        'severity': 'High',
        'survival_rate': 'Varies by grade (20-80%)',
        'stages': {
            'I': {
                'description': 'Low-grade glioma (Grade I)',
                'characteristics': 'Slow-growing, well-differentiated cells',
                'treatment_approach': 'Surgical removal with monitoring',
                'prognosis': 'Good - 80% 5-year survival'
            },
            'II': {
                'description': 'Low-grade glioma (Grade II)',
                'characteristics': 'Slow-growing but infiltrative',
                'treatment_approach': 'Surgery + radiation therapy',
                'prognosis': 'Moderate - 60% 5-year survival'
            },
            'III': {
                'description': 'Anaplastic glioma (Grade III)',
                'characteristics': 'Rapidly growing, anaplastic cells',
                'treatment_approach': 'Surgery + radiation + chemotherapy',
                'prognosis': 'Poor - 30% 5-year survival'
            },
            'IV': {
                'description': 'Glioblastoma (Grade IV)',
                'characteristics': 'Highly malignant, rapid growth',
                'treatment_approach': 'Aggressive multimodal therapy',
                'prognosis': 'Very poor - 15% 5-year survival'
            },
            'V': {
                'description': 'Recurrent/refractory glioblastoma',
                'characteristics': 'Treatment-resistant, widespread',
                'treatment_approach': 'Palliative care + experimental therapies',
                'prognosis': 'Extremely poor - 5% 5-year survival'
            }
        }
    },
    'meningioma': {
        'name': 'Meningioma',
        'description': 'A tumor that forms on membranes that cover the brain and spinal cord.',
        'cell_structure': 'Meningiomas typically show whorled patterns of spindle-shaped cells with psammoma bodies. They have well-defined borders and slow growth.',
        'symptoms': ['Headaches', 'Seizures', 'Weakness in limbs', 'Vision changes', 'Hearing loss'],
        'treatments': [
            'Surgical removal',
            'Radiation therapy for inoperable cases',
            'Watchful waiting for small, asymptomatic tumors',
            'Stereotactic radiosurgery'
        ],
        'prevention': [
            'Regular brain imaging for high-risk patients',
            'Avoid head trauma',
            'Maintain healthy lifestyle',
            'Monitor for symptoms'
        ],
        'severity': 'Low to Moderate',
        'survival_rate': '90-95% with treatment',
        'stages': {
            'I': {
                'description': 'Grade I meningioma',
                'characteristics': 'Benign, slow-growing, well-defined',
                'treatment_approach': 'Surgical removal or observation',
                'prognosis': 'Excellent - 95% survival rate'
            },
            'II': {
                'description': 'Grade II (atypical) meningioma',
                'characteristics': 'Moderate growth, some atypical features',
                'treatment_approach': 'Surgical removal + radiation',
                'prognosis': 'Good - 85% survival rate'
            },
            'III': {
                'description': 'Grade III (anaplastic) meningioma',
                'characteristics': 'Rapid growth, malignant features',
                'treatment_approach': 'Aggressive surgery + radiation',
                'prognosis': 'Moderate - 60% survival rate'
            },
            'IV': {
                'description': 'Recurrent anaplastic meningioma',
                'characteristics': 'Treatment-resistant, aggressive',
                'treatment_approach': 'Multimodal therapy + clinical trials',
                'prognosis': 'Poor - 30% survival rate'
            },
            'V': {
                'description': 'Metastatic meningioma',
                'characteristics': 'Distant spread, end-stage disease',
                'treatment_approach': 'Palliative care + experimental treatment',
                'prognosis': 'Very poor - 10% survival rate'
            }
        }
    },
    'notumor': {
        'name': 'No Tumor Detected',
        'description': 'No evidence of brain tumor found in the MRI scan.',
        'cell_structure': 'Normal brain tissue with regular cellular architecture, no abnormal cell proliferation detected.',
        'symptoms': 'None detected',
        'treatments': 'No treatment required',
        'prevention': [
            'Maintain healthy lifestyle',
            'Regular exercise',
            'Balanced diet',
            'Adequate sleep',
            'Stress management'
        ],
        'severity': 'None',
        'survival_rate': 'N/A',
        'stages': {
            'N/A': {
                'description': 'No tumor present',
                'characteristics': 'Normal brain tissue',
                'treatment_approach': 'No treatment required',
                'prognosis': 'Normal life expectancy'
            }
        }
    }
}

def analyze_image_features(image_path):
    """Analyze image features for detailed report"""
    try:
        # Load image for analysis
        img = cv2.imread(image_path)
        if img is None:
            return {}
        
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Basic image statistics
        mean_intensity = np.mean(gray)
        std_intensity = np.std(gray)
        
        # Edge detection
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
        
        # Texture analysis using GLCM-like features
        # Simple texture measure using local variance
        kernel = np.ones((5,5), np.float32)/25
        smooth = cv2.filter2D(gray, -1, kernel)
        texture_variance = np.var(gray - smooth)
        
        # Contour analysis
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_count = len(contours)
        
        return {
            'mean_intensity': round(mean_intensity, 2),
            'std_intensity': round(std_intensity, 2),
            'edge_density': round(edge_density * 100, 2),
            'texture_variance': round(texture_variance, 2),
            'contour_count': contour_count,
            'image_size': f"{img.shape[1]}x{img.shape[0]} pixels"
        }
    except Exception as e:
        return {}

from gradcam_utils import get_gradcam, save_gradcam, visualize_cell_structure, generate_growth_graph

# Helper function to predict tumor type
def predict_tumor(image_path):
    IMAGE_SIZE = 128
    img = load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
    img_array = img_to_array(img) / 255.0  # Normalize pixel values
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension

    predictions = model.predict(img_array)
    predicted_class_index = np.argmax(predictions, axis=1)[0]
    confidence_score = np.max(predictions, axis=1)[0]
    
    # Get all prediction scores
    all_scores = predictions[0]
    
    # Analyze image features
    image_features = analyze_image_features(image_path)
    
    tumor_type = class_labels[predicted_class_index]
    tumor_data = tumor_info[tumor_type].copy()
    
    # Predict tumor stage
    predicted_stage = predict_tumor_stage(tumor_type, image_features, confidence_score * 100)
    tumor_data['predicted_stage'] = predicted_stage
    
    # Get stage-specific information
    if predicted_stage in tumor_data['stages']:
        tumor_data['stage_info'] = tumor_data['stages'][predicted_stage]
    else:
        tumor_data['stage_info'] = tumor_data['stages'].get('I', tumor_data['stages']['N/A'])
    
    # Add prediction details
    tumor_data['confidence'] = round(confidence_score * 100, 2)
    tumor_data['prediction_scores'] = {
        'pituitary': round(all_scores[0] * 100, 2),
        'glioma': round(all_scores[1] * 100, 2),
        'notumor': round(all_scores[2] * 100, 2),
        'meningioma': round(all_scores[3] * 100, 2)
    }
    tumor_data['image_features'] = image_features
    tumor_data['analysis_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Generate Grad-CAM
    try:
        heatmap = get_gradcam(model, img_array, predicted_class_index)
        if heatmap is not None:
            # Generate filenames
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            heatmap_filename = f"{base_name}_heatmap.jpg"
            overlay_filename = f"{base_name}_gradcam.jpg"
            cell_filename = f"{base_name}_cells.jpg"
            graph_filename = f"{base_name}_growth.jpg"
            
            heatmap_path = os.path.join(os.path.dirname(image_path), heatmap_filename)
            overlay_path = os.path.join(os.path.dirname(image_path), overlay_filename)
            cell_path = os.path.join(os.path.dirname(image_path), cell_filename)
            graph_path = os.path.join(os.path.dirname(image_path), graph_filename)
            
            if save_gradcam(image_path, heatmap, heatmap_path, overlay_path):
                tumor_data['heatmap_path'] = heatmap_path
                tumor_data['gradcam_path'] = overlay_path
                tumor_data['heatmap_filename'] = heatmap_filename
                tumor_data['gradcam_filename'] = overlay_filename
                
                # Generate Cell Structure Visualization if tumor is detected
                if tumor_type != 'notumor':
                    if visualize_cell_structure(image_path, heatmap, cell_path):
                        tumor_data['cell_path'] = cell_path
                        tumor_data['cell_filename'] = cell_filename
                    
                    # Generate Growth Graph
                    if generate_growth_graph(tumor_type, predicted_stage, confidence_score * 100, graph_path):
                        tumor_data['graph_path'] = graph_path
                        tumor_data['graph_filename'] = graph_filename
                        
    except Exception as e:
        print(f"Error generating Grad-CAM in predict_tumor: {e}")
    
    return tumor_data

def predict_tumor_stage(tumor_type, image_features, confidence_score):
    """
    Predict tumor stage based on tumor type, image features, and confidence score
    """
    if tumor_type == 'notumor':
        return 'N/A'
    
    # Base stage prediction on image features and confidence
    mean_intensity = image_features.get('mean_intensity', 128)
    edge_density = image_features.get('edge_density', 0)
    texture_variance = image_features.get('texture_variance', 0)
    contour_count = image_features.get('contour_count', 0)
    
    # Normalize features for scoring
    intensity_score = (mean_intensity - 50) / 200  # Normalize to 0-1
    edge_score = edge_density / 100  # Already normalized
    texture_score = min(texture_variance / 1000, 1)  # Normalize texture
    contour_score = min(contour_count / 50, 1)  # Normalize contours
    
    # Calculate overall severity score
    severity_score = (
        intensity_score * 0.3 +
        edge_score * 0.25 +
        texture_score * 0.25 +
        contour_score * 0.2
    )
    
    # Adjust based on confidence score
    confidence_factor = confidence_score / 100
    final_score = severity_score * confidence_factor
    
    # Determine stage based on tumor type and score
    if tumor_type == 'pituitary':
        if final_score < 0.2:
            return 'I'
        elif final_score < 0.4:
            return 'II'
        elif final_score < 0.6:
            return 'III'
        elif final_score < 0.8:
            return 'IV'
        else:
            return 'V'
    
    elif tumor_type == 'glioma':
        if final_score < 0.15:
            return 'I'
        elif final_score < 0.35:
            return 'II'
        elif final_score < 0.55:
            return 'III'
        elif final_score < 0.75:
            return 'IV'
        else:
            return 'V'
    
    elif tumor_type == 'meningioma':
        if final_score < 0.25:
            return 'I'
        elif final_score < 0.45:
            return 'II'
        elif final_score < 0.65:
            return 'III'
        elif final_score < 0.85:
            return 'IV'
        else:
            return 'V'
    
    return 'I'  # Default stage

# Route for patient information form
@app.route('/patient_info', methods=['GET', 'POST'])
def patient_info():
    if request.method == 'POST':
        # Get patient information from form
        patient_info = {
            'name': request.form.get('name'),
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'contact': request.form.get('contact'),
            'email': request.form.get('email')
        }
        
        # Store patient info in session or pass to next step
        return render_template('upload.html', patient_info=patient_info)
    
    return render_template('patient_info.html')

# Route for file upload with patient info
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get patient information
        patient_info = {
            'name': request.form.get('name'),
            'age': int(request.form.get('age')),
            'gender': request.form.get('gender'),
            'contact': request.form.get('contact'),
            'email': request.form.get('email')
        }
        
        # Handle file upload
        file = request.files['file']
        if file:
            # Save the file
            file_location = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_location)

            # Predict the tumor
            result_data = predict_tumor(file_location)
            
            # Connect to database
            if db_manager.connect():
                try:
                    # Insert patient information
                    patient_id = db_manager.insert_patient(
                        patient_info['name'],
                        patient_info['age'],
                        patient_info['gender'],
                        patient_info['contact'],
                        patient_info['email']
                    )
                    
                    if patient_id:
                        # Generate PDF report
                        try:
                            pdf_path = generate_pdf_report(
                                patient_info, 
                                result_data, 
                                file_location
                            )
                            
                            # Verify PDF was created successfully
                            if os.path.exists(pdf_path):
                                # Add PDF path to result data (ensure it's the filename only)
                                result_data['pdf_path'] = os.path.basename(pdf_path)
                                print(f"PDF generated successfully at: {pdf_path}")
                                print(f"PDF filename: {os.path.basename(pdf_path)}")
                            else:
                                print(f"ERROR: PDF was not created at {pdf_path}")
                                result_data['pdf_path'] = None
                        except Exception as e:
                            print(f"Error generating PDF: {e}")
                            result_data['pdf_path'] = None
                            pdf_path = None
                        
                        # Determine prediction result
                        if result_data.get('name') == 'No Tumor Detected':
                            prediction_result = "No Tumor"
                        else:
                            prediction_result = "Tumor Detected"
                        
                        # Insert report into database
                        db_manager.insert_report(
                            patient_id=patient_id,
                            image_path=file_location,
                            pdf_path=pdf_path if pdf_path else "",
                            tumor_type=result_data.get('name'),
                            tumor_stage=result_data.get('predicted_stage'),
                            confidence_score=result_data.get('confidence'),
                            prediction_result=prediction_result,
                            image_features=json.dumps(result_data.get('image_features', {})),
                            doctor_notes=""
                        )
                        
                        result_data['patient_info'] = patient_info
                        
                finally:
                    db_manager.disconnect()

            # Return result along with image path for display
            return render_template('result.html', 
                                result_data=result_data, 
                                patient_info=patient_info,
                                file_path=f'/uploads/{file.filename}')

    return render_template('upload.html')

# Route for downloading PDF reports
@app.route('/download_pdf/<path:filename>')
def download_pdf(filename):
    try:
        # Ensure the reports directory exists
        reports_dir = os.path.join(os.getcwd(), 'reports')
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        # Check if file exists
        file_path = os.path.join(reports_dir, filename)
        print(f"Attempting to download: {filename}")
        print(f"Full file path: {file_path}")
        print(f"File exists: {os.path.exists(file_path)}")
        print(f"Current working directory: {os.getcwd()}")
        
        if not os.path.exists(file_path):
            # List files in reports directory for debugging
            if os.path.exists(reports_dir):
                files = os.listdir(reports_dir)
                print(f"Files in reports directory: {files}")
            return "File not found", 404
        
        # Use absolute path for send_from_directory
        return send_from_directory(
            directory=reports_dir,
            path=filename,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        return f"Error downloading file: {str(e)}", 500

# Route for downloading PDF by report ID
@app.route('/download_report_pdf/<int:report_id>')
def download_report_pdf(report_id):
    try:
        print(f"=== Download request for report ID: {report_id} ===")
        
        if db_manager.connect():
            try:
                # Get the report
                db_manager.cursor.execute("""
                    SELECT pdf_path FROM reports WHERE id = %s
                """, (report_id,))
                
                result = db_manager.cursor.fetchone()
                print(f"Database result: {result}")
                
                if not result or not result[0]:
                    print(f"No PDF path found for report {report_id}")
                    return "PDF not found for this report", 404
                
                pdf_path = result[0]
                filename = os.path.basename(pdf_path) if '/' in pdf_path else pdf_path
                print(f"PDF path from DB: {pdf_path}")
                print(f"Extracted filename: {filename}")
                
                # Ensure the reports directory exists
                reports_dir = os.path.join(os.getcwd(), 'reports')
                if not os.path.exists(reports_dir):
                    os.makedirs(reports_dir)
                    print(f"Created reports directory: {reports_dir}")
                
                # Check if file exists
                file_path = os.path.join(reports_dir, filename)
                print(f"Attempting to download report {report_id}: {filename}")
                print(f"Full file path: {file_path}")
                print(f"File exists: {os.path.exists(file_path)}")
                print(f"Current working directory: {os.getcwd()}")
                
                if not os.path.exists(file_path):
                    # Try to regenerate the PDF if it doesn't exist
                    print(f"PDF file not found, attempting to regenerate for report {report_id}")
                    regenerate_result = regenerate_pdf_with_notes(report_id)
                    if hasattr(regenerate_result, 'status_code') and regenerate_result.status_code == 200:
                        # Try downloading again
                        if os.path.exists(file_path):
                            print(f"PDF regenerated successfully, now downloading: {file_path}")
                            return send_from_directory(
                                directory=reports_dir,
                                path=filename,
                                as_attachment=True,
                                download_name=filename
                            )
                    print(f"Could not regenerate PDF for report {report_id}")
                    return "PDF file not found and could not be regenerated", 404
                
                # Use absolute path for send_from_directory
                print(f"Downloading existing PDF: {file_path}")
                return send_from_directory(
                    directory=reports_dir,
                    path=filename,
                    as_attachment=True,
                    download_name=filename
                )
                
            finally:
                db_manager.disconnect()
        else:
            print("Failed to connect to database")
            return "Database connection failed", 500
            
    except Exception as e:
        print(f"Error downloading report PDF: {e}")
        import traceback
        traceback.print_exc()
        return f"Error downloading file: {str(e)}", 500

# Route for listing available PDF files (for debugging)
@app.route('/list_pdfs')
def list_pdfs():
    try:
        reports_dir = os.path.join(os.getcwd(), 'reports')
        if os.path.exists(reports_dir):
            files = os.listdir(reports_dir)
            pdf_files = [f for f in files if f.endswith('.pdf')]
            return jsonify({
                "pdf_files": pdf_files,
                "reports_dir": reports_dir,
                "current_dir": os.getcwd(),
                "dir_exists": os.path.exists(reports_dir)
            })
        else:
            return jsonify({
                "pdf_files": [], 
                "error": "Reports directory not found",
                "reports_dir": reports_dir,
                "current_dir": os.getcwd()
            })
    except Exception as e:
        return jsonify({"error": str(e)})

# Route for testing PDF download with existing file
@app.route('/test_pdf_download')
def test_pdf_download():
    try:
        reports_dir = os.path.join(os.getcwd(), 'reports')
        if os.path.exists(reports_dir):
            files = os.listdir(reports_dir)
            pdf_files = [f for f in files if f.endswith('.pdf')]
            if pdf_files:
                # Try to download the first PDF file
                test_filename = pdf_files[0]
                return download_pdf(test_filename)
            else:
                return "No PDF files found in reports directory"
        else:
            return "Reports directory not found"
    except Exception as e:
        return f"Error: {str(e)}"

# Route for checking PDF status
@app.route('/check_pdf_status')
def check_pdf_status():
    try:
        reports_dir = os.path.join(os.getcwd(), 'reports')
        status = {
            "current_dir": os.getcwd(),
            "reports_dir": reports_dir,
            "reports_dir_exists": os.path.exists(reports_dir),
            "files": []
        }
        
        if os.path.exists(reports_dir):
            files = os.listdir(reports_dir)
            for file in files:
                file_path = os.path.join(reports_dir, file)
                status["files"].append({
                    "name": file,
                    "size": os.path.getsize(file_path) if os.path.isfile(file_path) else 0,
                    "exists": os.path.exists(file_path)
                })
        
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to debug database structure for a specific report
@app.route('/debug_report/<int:report_id>')
def debug_report(report_id):
    try:
        print(f"=== Debugging report ID: {report_id} ===")
        
        if db_manager.connect():
            try:
                # Get the report details
                db_manager.cursor.execute("""
                    SELECT r.*, p.name, p.age, p.gender, p.contact, p.email
                    FROM reports r
                    JOIN patients p ON r.patient_id = p.id
                    WHERE r.id = %s
                """, (report_id,))
                
                report = db_manager.cursor.fetchone()
                if not report:
                    return jsonify({"error": "Report not found"})
                
                # Get column names
                db_manager.cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'reports' 
                    ORDER BY ordinal_position
                """)
                report_columns = [col[0] for col in db_manager.cursor.fetchall()]
                
                db_manager.cursor.execute("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'patients' 
                    ORDER BY ordinal_position
                """)
                patient_columns = [col[0] for col in db_manager.cursor.fetchall()]
                
                debug_info = {
                    "report_id": report_id,
                    "total_columns": len(report),
                    "report_columns": report_columns,
                    "patient_columns": patient_columns,
                    "report_data": {
                        "id": report[0] if len(report) > 0 else None,
                        "patient_id": report[1] if len(report) > 1 else None,
                        "image_path": report[2] if len(report) > 2 else None,
                        "pdf_path": report[3] if len(report) > 3 else None,
                        "tumor_type": report[4] if len(report) > 4 else None,
                        "tumor_stage": report[5] if len(report) > 5 else None,
                        "confidence_score": report[6] if len(report) > 6 else None,
                        "prediction_result": report[7] if len(report) > 7 else None,
                        "image_features": report[8] if len(report) > 8 else None,
                        "doctor_notes": report[9] if len(report) > 9 else None,
                        "created_at": report[10] if len(report) > 10 else None,
                    },
                    "patient_data": {
                        "name": report[11] if len(report) > 11 else None,
                        "age": report[12] if len(report) > 12 else None,
                        "gender": report[13] if len(report) > 13 else None,
                        "contact": report[14] if len(report) > 14 else None,
                        "email": report[15] if len(report) > 15 else None,
                    }
                }
                
                return jsonify(debug_info)
                
            except Exception as e:
                return jsonify({"error": f"Database error: {str(e)}"})
            finally:
                db_manager.disconnect()
        else:
            return jsonify({"error": "Database connection failed"})
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"})

# Route to test PDF download for a specific report
@app.route('/test_download/<int:report_id>')
def test_download(report_id):
    try:
        print(f"=== Testing download for report ID: {report_id} ===")
        
        if db_manager.connect():
            try:
                # Get the report details
                db_manager.cursor.execute("""
                    SELECT r.*, p.name, p.age, p.gender, p.contact, p.email
                    FROM reports r
                    JOIN patients p ON r.patient_id = p.id
                    WHERE r.id = %s
                """, (report_id,))
                
                report = db_manager.cursor.fetchone()
                if not report:
                    return jsonify({"error": "Report not found"})
                
                pdf_path = report[3]  # pdf_path is at index 3
                filename = os.path.basename(pdf_path) if '/' in pdf_path else pdf_path
                
                reports_dir = os.path.join(os.getcwd(), 'reports')
                file_path = os.path.join(reports_dir, filename)
                
                return jsonify({
                    "report_id": report_id,
                    "pdf_path": pdf_path,
                    "filename": filename,
                    "file_path": file_path,
                    "file_exists": os.path.exists(file_path),
                    "reports_dir": reports_dir,
                    "reports_dir_exists": os.path.exists(reports_dir)
                })
                
            finally:
                db_manager.disconnect()
        else:
            return jsonify({"error": "Database connection failed"})
            
    except Exception as e:
        return jsonify({"error": str(e)})

# Route to delete a report
@app.route('/delete_report/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    try:
        print(f"=== Deleting report ID: {report_id} ===")
        
        if db_manager.connect():
            try:
                # First, get the report details to delete associated files
                db_manager.cursor.execute("""
                    SELECT pdf_path, image_path FROM reports WHERE id = %s
                """, (report_id,))
                
                report = db_manager.cursor.fetchone()
                if not report:
                    return jsonify({"status": "error", "message": "Report not found"})
                
                pdf_path = report[0]
                image_path = report[1]
                
                # Delete PDF file if it exists
                if pdf_path:
                    try:
                        filename = os.path.basename(pdf_path) if '/' in pdf_path else pdf_path
                        reports_dir = os.path.join(os.getcwd(), 'reports')
                        pdf_file_path = os.path.join(reports_dir, filename)
                        
                        if os.path.exists(pdf_file_path):
                            os.remove(pdf_file_path)
                            print(f"Deleted PDF file: {pdf_file_path}")
                    except Exception as e:
                        print(f"Error deleting PDF file: {e}")
                
                # Delete uploaded image if it exists
                if image_path:
                    try:
                        uploads_dir = os.path.join(os.getcwd(), 'uploads')
                        image_file_path = os.path.join(uploads_dir, os.path.basename(image_path))
                        
                        if os.path.exists(image_file_path):
                            os.remove(image_file_path)
                            print(f"Deleted image file: {image_file_path}")
                    except Exception as e:
                        print(f"Error deleting image file: {e}")
                
                # Delete the report from database
                db_manager.cursor.execute("DELETE FROM reports WHERE id = %s", (report_id,))
                db_manager.connection.commit()
                
                print(f"Successfully deleted report ID: {report_id}")
                return jsonify({"status": "success", "message": "Report deleted successfully"})
                
            finally:
                db_manager.disconnect()
        else:
            return jsonify({"status": "error", "message": "Database connection failed"})
            
    except Exception as e:
        print(f"Error deleting report: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"status": "error", "message": f"Error deleting report: {str(e)}"})

# Route for debug page
@app.route('/debug')
def debug_page():
    return render_template('debug.html')

# Route for viewing all reports
@app.route('/reports')
def view_reports():
    if db_manager.connect():
        try:
            reports = db_manager.get_all_reports()
            return render_template('reports.html', reports=reports)
        finally:
            db_manager.disconnect()
    return render_template('reports.html', reports=[])

# Route for initializing database
@app.route('/init_db')
def init_database_route():
    if db_manager.connect():
        try:
            db_manager.create_tables()
            return jsonify({"status": "success", "message": "Database initialized successfully"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
        finally:
            db_manager.disconnect()
    return jsonify({"status": "error", "message": "Could not connect to database"})

# Route for adding doctor's notes
@app.route('/add_notes/<int:report_id>', methods=['POST'])
def add_doctor_notes(report_id):
    notes = request.form.get('notes', '')
    if db_manager.connect():
        try:
            db_manager.update_doctor_notes(report_id, notes)
            return jsonify({"status": "success", "message": "Notes added successfully"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
        finally:
            db_manager.disconnect()
    return jsonify({"status": "error", "message": "Could not connect to database"})

# Route to get a specific report by ID
@app.route('/get_report/<int:report_id>')
def get_report(report_id):
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
            if report:
                return jsonify({
                    "status": "success",
                    "report": {
                        "id": report[0],
                        "patient_id": report[1],
                        "image_path": report[2],
                        "pdf_path": report[3],
                        "tumor_type": report[4],
                        "tumor_stage": report[5],
                        "confidence_score": report[6],
                        "prediction_result": report[7],
                        "image_features": report[8],
                        "doctor_notes": report[9],
                        "created_at": report[10],
                        "patient_name": report[11],
                        "patient_age": report[12],
                        "patient_gender": report[13],
                        "patient_contact": report[14],
                        "patient_email": report[15]
                    }
                })
            else:
                return jsonify({"status": "error", "message": "Report not found"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
        finally:
            db_manager.disconnect()
    return jsonify({"status": "error", "message": "Could not connect to database"})

# Route to regenerate PDF with doctor's notes
@app.route('/regenerate_pdf/<int:report_id>')
def regenerate_pdf_with_notes(report_id):
    print(f"=== Regenerating PDF for report ID: {report_id} ===")
    
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
                print(f"Report not found for ID: {report_id}")
                return jsonify({"status": "error", "message": "Report not found"})
            
            print(f"Report data length: {len(report)}")
            print(f"Report data: {report}")
            
            # Check if we have enough columns
            if len(report) < 16:
                print(f"Error: Expected at least 16 columns, got {len(report)}")
                return jsonify({"status": "error", "message": f"Database structure error: Expected 16 columns, got {len(report)}"})
            
            # Prepare patient info - correct indices for joined query
            # Reports table has 11 columns (0-10), then patients table has 5 columns (11-15)
            patient_info = {
                'name': report[11] if len(report) > 11 else 'Unknown',      # p.name
                'age': report[12] if len(report) > 12 else 0,              # p.age
                'gender': report[13] if len(report) > 13 else 'Unknown',   # p.gender
                'contact': report[14] if len(report) > 14 else '',         # p.contact
                'email': report[15] if len(report) > 15 else ''            # p.email
            }
            
            print(f"Patient info: {patient_info}")
            
            # Prepare result data - correct indices for reports table
            result_data = {
                'name': report[4] if len(report) > 4 and report[4] else 'No Tumor Detected',  # r.tumor_type
                'predicted_stage': report[5] if len(report) > 5 and report[5] else 'N/A',     # r.tumor_stage
                'confidence': report[6] if len(report) > 6 and report[6] else 0,              # r.confidence_score
                'description': 'Brain tumor analysis report',
                'severity': 'Moderate' if (len(report) > 4 and report[4] and report[4] != 'No Tumor Detected') else 'None',
                'survival_rate': '85-95% with proper treatment' if (len(report) > 4 and report[4] and report[4] != 'No Tumor Detected') else 'N/A'
            }
            
            print(f"Result data: {result_data}")
            
            # Get doctor's notes
            doctor_notes = report[9] if len(report) > 9 and report[9] else ""  # r.doctor_notes
            print(f"Doctor notes: {doctor_notes}")
            
            # Get image path
            image_path = report[2] if len(report) > 2 and report[2] else ""  # r.image_path
            print(f"Image path: {image_path}")
            
            if not image_path:
                return jsonify({"status": "error", "message": "Image path not found in database"})
            
            # Check if image exists
            if not os.path.exists(image_path):
                print(f"Warning: Image file not found at {image_path}")
                # Try to find the image in uploads directory
                uploads_dir = os.path.join(os.getcwd(), 'uploads')
                image_filename = os.path.basename(image_path)
                alt_image_path = os.path.join(uploads_dir, image_filename)
                if os.path.exists(alt_image_path):
                    image_path = alt_image_path
                    print(f"Found image at alternative path: {image_path}")
                else:
                    print(f"Image not found at alternative path either: {alt_image_path}")
            
            # Generate new PDF with notes
            try:
                print("Calling generate_pdf_report...")
                new_pdf_path = generate_pdf_report(
                    patient_info, 
                    result_data, 
                    image_path,
                    "reports",
                    doctor_notes
                )
                
                print(f"Generated PDF path: {new_pdf_path}")
                
                # Update the database with new PDF path
                db_manager.cursor.execute("""
                    UPDATE reports 
                    SET pdf_path = %s 
                    WHERE id = %s
                """, (new_pdf_path, report_id))
                
                db_manager.connection.commit()
                print(f"Database updated with new PDF path: {new_pdf_path}")
                
                return jsonify({
                    "status": "success", 
                    "message": "PDF regenerated successfully",
                    "pdf_filename": os.path.basename(new_pdf_path)
                })
                
            except Exception as e:
                print(f"Error generating PDF: {e}")
                import traceback
                traceback.print_exc()
                return jsonify({"status": "error", "message": f"Error generating PDF: {str(e)}"})
                
        except Exception as e:
            print(f"Error in regenerate_pdf_with_notes: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({"status": "error", "message": str(e)})
        finally:
            db_manager.disconnect()
    else:
        print("Failed to connect to database")
        return jsonify({"status": "error", "message": "Could not connect to database"})

# Route for doctor's interface
@app.route('/doctor')
def doctor_interface():
    if db_manager.connect():
        try:
            reports = db_manager.get_all_reports()
            return render_template('doctor_interface.html', reports=reports)
        finally:
            db_manager.disconnect()
    return render_template('doctor_interface.html', reports=[])

# Route for the main page (index.html)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        file = request.files['file']
        if file:
            # Save the file
            file_location = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_location)

            # Predict the tumor
            result_data = predict_tumor(file_location)
            
            # Create default patient info for direct uploads
            default_patient_info = {
                'name': 'Anonymous User',
                'age': 30,
                'gender': 'Not Specified',
                'contact': 'Not Provided',
                'email': 'Not Provided'
            }
            
            # Connect to database and create report
            if db_manager.connect():
                try:
                    # Insert patient information
                    patient_id = db_manager.insert_patient(
                        default_patient_info['name'],
                        default_patient_info['age'],
                        default_patient_info['gender'],
                        default_patient_info['contact'],
                        default_patient_info['email']
                    )
                    
                    if patient_id:
                        # Generate PDF report
                        try:
                            print(f"Starting PDF generation...")
                            print(f"Patient info: {default_patient_info}")
                            print(f"Result data keys: {result_data.keys()}")
                            print(f"Image path: {file_location}")
                            print(f"Image exists: {os.path.exists(file_location)}")
                            
                            pdf_path = generate_pdf_report(
                                default_patient_info, 
                                result_data, 
                                file_location,
                                "reports"
                            )
                            
                            print(f"PDF generation completed. Path: {pdf_path}")
                            
                            # Verify PDF was created successfully
                            if pdf_path and os.path.exists(pdf_path):
                                result_data['pdf_path'] = os.path.basename(pdf_path)
                                print(f"✅ PDF generated successfully at: {pdf_path}")
                                print(f"✅ PDF filename: {os.path.basename(pdf_path)}")
                            else:
                                print(f"❌ ERROR: PDF was not created")
                                result_data['pdf_path'] = None
                                pdf_path = None
                        except Exception as e:
                            print(f"❌ Error generating PDF: {e}")
                            import traceback
                            traceback.print_exc()
                            result_data['pdf_path'] = None
                            pdf_path = None
                        
                        # Determine prediction result
                        if result_data.get('name') == 'No Tumor Detected':
                            prediction_result = "No Tumor"
                        else:
                            prediction_result = "Tumor Detected"
                        
                        # Insert report into database
                        db_manager.insert_report(
                            patient_id=patient_id,
                            image_path=file_location,
                            pdf_path=pdf_path if pdf_path else "",
                            tumor_type=result_data.get('name'),
                            tumor_stage=result_data.get('predicted_stage'),
                            confidence_score=result_data.get('confidence'),
                            prediction_result=prediction_result,
                            image_features=json.dumps(result_data.get('image_features', {})),
                            doctor_notes=""
                        )
                        
                        result_data['patient_info'] = default_patient_info
                        
                finally:
                    db_manager.disconnect()

            # Return result along with image path for display
            return render_template('index.html', 
                                result_data=result_data, 
                                file_path=f'/uploads/{file.filename}')

    return render_template('index.html', result_data=None)

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API route for AJAX requests
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save the file
    file_location = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_location)
    
    # Predict the tumor
    result_data = predict_tumor(file_location)
    
    return jsonify(result_data)

# Chatbot API routes
@app.route('/chatbot/message', methods=['POST'])
def chatbot_message():
    """Handle chatbot messages"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        user_context = data.get('context', None)
        
        if not user_message.strip():
            return jsonify({
                'success': False,
                'error': 'Message cannot be empty'
            }), 400
        
        # Get response from chatbot
        response = medical_chatbot.get_response(user_message, user_context)
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'response': 'I apologize, but I encountered an error. Please try again.'
        }), 500

@app.route('/chatbot/suggestions', methods=['GET'])
def chatbot_suggestions():
    """Get suggested questions for the chatbot"""
    try:
        suggestions = medical_chatbot.get_suggested_questions()
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/chatbot/clear', methods=['POST'])
def clear_chatbot_history():
    """Clear chatbot conversation history"""
    try:
        medical_chatbot.clear_history()
        return jsonify({
            'success': True,
            'message': 'Conversation history cleared'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    """Generate PDF report from analysis data"""
    try:
        # Get result data from request
        result_data_json = request.form.get('result_data')
        if not result_data_json:
            return jsonify({
                'success': False,
                'error': 'No analysis data provided'
            }), 400
        
        result_data = json.loads(result_data_json)
        
        # Create default patient info
        default_patient_info = {
            'name': 'Anonymous User',
            'age': 30,
            'gender': 'Not Specified',
            'contact': 'Not Provided',
            'email': 'Not Provided'
        }
        
        # Find the image file
        image_filename = None
        uploads_dir = os.path.join(os.getcwd(), 'uploads')
        if os.path.exists(uploads_dir):
            files = os.listdir(uploads_dir)
            if files:
                # Get the most recent image file
                image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if image_files:
                    image_filename = image_files[-1]  # Get the last uploaded file
        
        if not image_filename:
            return jsonify({
                'success': False,
                'error': 'No image file found for report generation'
            }), 400
        
        image_path = os.path.join(uploads_dir, image_filename)
        
        print(f"Generating report for image: {image_path}")
        print(f"Image exists: {os.path.exists(image_path)}")
        
        # Generate PDF report
        pdf_path = generate_pdf_report(
            default_patient_info,
            result_data,
            image_path,
            "reports"
        )
        
        if pdf_path and os.path.exists(pdf_path):
            pdf_filename = os.path.basename(pdf_path)
            return jsonify({
                'success': True,
                'pdf_path': pdf_filename,
                'message': 'Report generated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to generate PDF report'
            }), 500
            
    except Exception as e:
        print(f"Error in generate_report: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
