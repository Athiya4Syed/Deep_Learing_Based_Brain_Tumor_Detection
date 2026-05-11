from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os
from datetime import datetime
import json

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles for the report"""
        # Header style
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))
        
        # Subheader style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            fontName='Helvetica-Bold'
        ))
        
        # Normal text style
        self.styles.add(ParagraphStyle(
            name='CustomNormal',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        # Bold text style
        self.styles.add(ParagraphStyle(
            name='CustomBold',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6,
            fontName='Helvetica-Bold'
        ))
    
    def create_report(self, patient_info, result_data, image_path, output_path, doctor_notes=""):
        """Create a complete PDF report"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # Add header
        story.append(Paragraph("Brain Tumor Detection Report", self.styles['CustomHeader']))
        story.append(Spacer(1, 20))
        
        # Add report generation date
        story.append(Paragraph(f"Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
                              self.styles['CustomNormal']))
        story.append(Spacer(1, 30))
        
        # Add patient information section
        story.extend(self.create_patient_info_section(patient_info))
        story.append(Spacer(1, 20))
        
        # Add prediction results section
        story.extend(self.create_prediction_section(result_data))
        story.append(Spacer(1, 20))
        
        # Add image section
        if os.path.exists(image_path):
            story.extend(self.create_image_section(image_path, result_data))
            story.append(Spacer(1, 20))
        
        # Add detailed analysis section
        story.extend(self.create_analysis_section(result_data))
        story.append(Spacer(1, 20))
        
        # Add doctor's notes section
        story.extend(self.create_doctors_notes_section(doctor_notes))
        story.append(Spacer(1, 30))
        
        # Add footer
        story.extend(self.create_footer())
        
        # Build PDF
        doc.build(story)
        return output_path
    
    def create_patient_info_section(self, patient_info):
        """Create patient information section"""
        story = []
        
        story.append(Paragraph("Patient Information", self.styles['CustomSubHeader']))
        
        # Create patient info table
        patient_data = [
            ['Name:', patient_info.get('name', 'N/A')],
            ['Age:', str(patient_info.get('age', 'N/A'))],
            ['Gender:', patient_info.get('gender', 'N/A')],
            ['Contact:', patient_info.get('contact', 'N/A')],
            ['Email:', patient_info.get('email', 'N/A')]
        ]
        
        patient_table = Table(patient_data, colWidths=[1.5*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(patient_table)
        return story
    
    def create_prediction_section(self, result_data):
        """Create prediction results section"""
        story = []
        
        story.append(Paragraph("Prediction Results", self.styles['CustomSubHeader']))
        
        # Determine prediction result
        if result_data.get('name') == 'No Tumor Detected':
            prediction_result = "No Tumor"
        else:
            prediction_result = "Tumor Detected"
        
        # Create prediction table
        prediction_data = [
            ['Prediction Result:', prediction_result],
            ['Tumor Type:', result_data.get('name', 'N/A')],
            ['Confidence Score:', f"{result_data.get('confidence', 0)}%"],
            ['Tumor Stage:', result_data.get('predicted_stage', 'N/A')]
        ]
        
        prediction_table = Table(prediction_data, colWidths=[2*inch, 3.5*inch])
        prediction_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(prediction_table)
        return story
    
    def create_image_section(self, image_path, result_data=None):
        """Create image section"""
        story = []
        
        story.append(Paragraph("MRI Image Analysis", self.styles['CustomSubHeader']))
        
        try:
            # Check if image file exists
            if not os.path.exists(image_path):
                story.append(Paragraph("Image file not found. Please ensure the uploaded image is available.", self.styles['CustomNormal']))
                return story
            
            # Create a table for images (Original, Heatmap, Grad-CAM, Cell Division)
            images_row = []
            
            # Original Image
            img = Image(image_path, width=1.5*inch, height=1.5*inch)
            images_row.append([img, Paragraph("Original MRI", self.styles['CustomNormal'])])
            
            # Grad-CAM Image
            if result_data and result_data.get('gradcam_path') and os.path.exists(result_data['gradcam_path']):
                gradcam_img = Image(result_data['gradcam_path'], width=1.5*inch, height=1.5*inch)
                images_row.append([gradcam_img, Paragraph("Grad-CAM", self.styles['CustomNormal'])])
                
            # Heatmap Image
            if result_data and result_data.get('heatmap_path') and os.path.exists(result_data['heatmap_path']):
                heatmap_img = Image(result_data['heatmap_path'], width=1.5*inch, height=1.5*inch)
                images_row.append([heatmap_img, Paragraph("Heatmap", self.styles['CustomNormal'])])
                
            # Cell Structure Image
            if result_data and result_data.get('cell_path') and os.path.exists(result_data['cell_path']):
                cell_img = Image(result_data['cell_path'], width=1.5*inch, height=1.5*inch)
                images_row.append([cell_img, Paragraph("Cell Structure", self.styles['CustomNormal'])])
            
            # Create table for images
            if len(images_row) > 0:
                # Flatten the list for the table
                table_data = [
                    [item[0] for item in images_row],
                    [item[1] for item in images_row]
                ]
                
                # Calculate column widths based on number of images
                col_width = 7.0 / len(images_row) * inch
                
                img_table = Table(table_data, colWidths=[col_width] * len(images_row))
                img_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ]))
                story.append(img_table)
            
            # Add Growth Graph if available
            if result_data and result_data.get('graph_path') and os.path.exists(result_data['graph_path']):
                story.append(Spacer(1, 10))
                story.append(Paragraph("Tumor Growth Analysis", self.styles['CustomSubHeader']))
                
                graph_img = Image(result_data['graph_path'], width=6*inch, height=3.6*inch)
                graph_img.hAlign = 'CENTER'
                story.append(graph_img)
                story.append(Paragraph("Figure: Projected tumor progression based on current stage and type.", self.styles['CustomNormal']))
            
            # Add image features if available
            if result_data and result_data.get('image_features'):
                features = result_data['image_features']
                story.append(Spacer(1, 10))
                story.append(Paragraph("Image Analysis Features:", self.styles['CustomBold']))
                
                feature_data = [
                    ['Image Size:', features.get('image_size', 'N/A')],
                    ['Mean Intensity:', str(features.get('mean_intensity', 'N/A'))],
                    ['Edge Density:', f"{features.get('edge_density', 0)}%"],
                    ['Contour Count:', str(features.get('contour_count', 'N/A'))]
                ]
                
                feature_table = Table(feature_data, colWidths=[2*inch, 3.5*inch])
                feature_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ]))
                
                story.append(feature_table)
                
        except Exception as e:
            story.append(Paragraph(f"Error loading image: {str(e)}", self.styles['CustomNormal']))
            print(f"Error in create_image_section: {e}")
        
        return story
    
    def create_analysis_section(self, result_data):
        """Create detailed analysis section"""
        story = []
        
        story.append(Paragraph("Detailed Analysis", self.styles['CustomSubHeader']))
        
        # Add tumor description
        if result_data.get('description'):
            story.append(Paragraph(f"<b>Description:</b> {result_data['description']}", 
                                  self.styles['CustomNormal']))
            story.append(Spacer(1, 10))
        
        # Add cell structure analysis
        if result_data.get('cell_structure'):
            story.append(Paragraph(f"<b>Cell Structure Analysis:</b> {result_data['cell_structure']}", 
                                  self.styles['CustomNormal']))
            story.append(Spacer(1, 10))
        
        # Add stage information if available
        if result_data.get('stage_info'):
            stage_info = result_data['stage_info']
            story.append(Paragraph(f"<b>Stage Description:</b> {stage_info.get('description', 'N/A')}", 
                                  self.styles['CustomNormal']))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Characteristics:</b> {stage_info.get('characteristics', 'N/A')}", 
                                  self.styles['CustomNormal']))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Recommended Treatment:</b> {stage_info.get('treatment_approach', 'N/A')}", 
                                  self.styles['CustomNormal']))
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"<b>Prognosis:</b> {stage_info.get('prognosis', 'N/A')}", 
                                  self.styles['CustomNormal']))
            story.append(Spacer(1, 10))
        
        # Add symptoms if available
        if result_data.get('symptoms') and result_data['symptoms'] != 'None detected':
            symptoms_text = ", ".join(result_data['symptoms'])
            story.append(Paragraph(f"<b>Common Symptoms:</b> {symptoms_text}", 
                                  self.styles['CustomNormal']))
            story.append(Spacer(1, 10))
        
        # Add treatments if available
        if result_data.get('treatments') and result_data['treatments'] != 'No treatment required':
            treatments_text = ", ".join(result_data['treatments'])
            story.append(Paragraph(f"<b>Treatment Options:</b> {treatments_text}", 
                                  self.styles['CustomNormal']))
            story.append(Spacer(1, 10))
        
        # Add risk assessment
        risk_data = [
            ['Severity:', result_data.get('severity', 'N/A')],
            ['Survival Rate:', result_data.get('survival_rate', 'N/A')]
        ]
        
        risk_table = Table(risk_data, colWidths=[1.5*inch, 4*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        
        story.append(Paragraph("Risk Assessment:", self.styles['CustomBold']))
        story.append(risk_table)
        
        return story
    
    def create_doctors_notes_section(self, doctor_notes=""):
        """Create doctor's notes section"""
        story = []
        
        story.append(Paragraph("Doctor's Notes", self.styles['CustomSubHeader']))
        
        if doctor_notes:
            # Display existing doctor's notes
            story.append(Paragraph(f"<b>Current Notes:</b>", self.styles['CustomBold']))
            story.append(Paragraph(doctor_notes, self.styles['CustomNormal']))
            story.append(Spacer(1, 10))
        
        # Create additional space for more notes
        notes_data = [
            ['Additional Notes:', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', ''],
            ['', '']
        ]
        
        notes_table = Table(notes_data, colWidths=[1*inch, 4.5*inch])
        notes_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        story.append(notes_table)
        story.append(Spacer(1, 10))
        story.append(Paragraph("Doctor's Signature: _________________", self.styles['CustomNormal']))
        story.append(Paragraph("Date: _________________", self.styles['CustomNormal']))
        
        return story
    
    def create_footer(self):
        """Create footer section"""
        story = []
        
        story.append(Spacer(1, 20))
        story.append(Paragraph("_" * 80, self.styles['CustomNormal']))
        story.append(Spacer(1, 10))
        story.append(Paragraph("This report is generated by an AI-powered brain tumor detection system.", 
                              self.styles['CustomNormal']))
        story.append(Paragraph("For clinical decisions, please consult with qualified medical professionals.", 
                              self.styles['CustomNormal']))
        story.append(Paragraph("Report ID: " + datetime.now().strftime("%Y%m%d%H%M%S"), 
                              self.styles['CustomNormal']))
        
        return story

# Function to generate report
def generate_pdf_report(patient_info, result_data, image_path, output_dir="reports", doctor_notes=""):
    """Generate PDF report and return the file path"""
    
    # Get absolute path for output directory
    current_dir = os.getcwd()
    abs_output_dir = os.path.join(current_dir, output_dir)
    
    # Create reports directory if it doesn't exist
    if not os.path.exists(abs_output_dir):
        os.makedirs(abs_output_dir)
        print(f"Created reports directory: {abs_output_dir}")
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    patient_name = patient_info.get('name', 'Unknown').replace(' ', '_')
    filename = f"BrainTumor_Report_{patient_name}_{timestamp}.pdf"
    output_path = os.path.join(abs_output_dir, filename)
    
    print(f"Generating PDF at: {output_path}")
    print(f"Image path: {image_path}")
    print(f"Image exists: {os.path.exists(image_path)}")
    print(f"Output directory exists: {os.path.exists(abs_output_dir)}")
    
    try:
        # Generate PDF
        generator = PDFReportGenerator()
        generator.create_report(patient_info, result_data, image_path, output_path, doctor_notes)
        
        # Verify PDF was created
        if os.path.exists(output_path):
            print(f"PDF successfully created: {output_path}")
            print(f"PDF file size: {os.path.getsize(output_path)} bytes")
            return output_path
        else:
            print(f"ERROR: PDF was not created at {output_path}")
            return None
            
    except Exception as e:
        print(f"Error during PDF generation: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test the PDF generator
    test_patient = {
        'name': 'John Doe',
        'age': 45,
        'gender': 'Male',
        'contact': '+1234567890',
        'email': 'john.doe@email.com'
    }
    
    test_result = {
        'name': 'Pituitary Tumor',
        'predicted_stage': 'II',
        'confidence': 85.5,
        'description': 'A tumor that forms in the pituitary gland.',
        'severity': 'Moderate',
        'survival_rate': '85-95% with proper treatment'
    }
    
    generate_pdf_report(test_patient, test_result, "test_image.jpg", "test_reports")
