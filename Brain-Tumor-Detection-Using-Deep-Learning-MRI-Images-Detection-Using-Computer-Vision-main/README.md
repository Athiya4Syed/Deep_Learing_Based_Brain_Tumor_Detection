# ResNet-50 Based Intelligent System for Brain Tumor Detection

A modern, AI-powered web application for brain tumor detection using deep learning and computer vision. This system provides comprehensive analysis of MRI images with detailed reports including cell structure analysis, treatment recommendations, and prevention measures.

## 🚀 Features

### Modern Interface
- **Dark Theme Design**: Sleek, modern interface with purple/blue gradients inspired by cutting-edge AI applications
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Drag & Drop Upload**: Intuitive file upload with drag-and-drop functionality
- **Real-time Analysis**: Instant feedback with loading animations and progress indicators

### Advanced AI Analysis
- **ResNet-50 Model**: State-of-the-art deep learning model for accurate tumor detection
- **Multi-class Classification**: Detects four types of brain conditions:
  - Pituitary Tumor
  - Glioma
  - Meningioma
  - No Tumor (Normal)

### Comprehensive Reports
- **Cell Structure Analysis**: Detailed microscopic analysis of tissue characteristics
- **Image Statistics**: Advanced image processing metrics including:
  - Mean intensity analysis
  - Edge density calculation
  - Texture variance measurement
  - Contour analysis
- **Medical Information**: Complete medical context including:
  - Tumor description and characteristics
  - Common symptoms
  - Treatment options
  - Prevention measures
  - Risk assessment and survival rates

### Technical Features
- **Image Processing**: Advanced computer vision analysis using OpenCV
- **Confidence Scoring**: Probability-based predictions with confidence levels
- **Detailed Logging**: Timestamped analysis with complete audit trail
- **API Support**: RESTful API endpoints for integration

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Brain-Tumor-Detection-Using-Deep-Learning-MRI-Images-Detection-Using-Computer-Vision-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
├── main.py                 # Main Flask application
├── train_model.py          # Model training script
├── models/
│   └── model.h5           # Pre-trained ResNet-50 model
├── templates/
│   └── index.html         # Modern web interface
├── uploads/               # Uploaded image storage
├── datasets/              # Training and testing datasets
│   ├── Training/
│   │   ├── glioma/
│   │   ├── meningioma/
│   │   ├── notumor/
│   │   └── pituitary/
│   └── Testing/
│       ├── glioma/
│       ├── meningioma/
│       ├── notumor/
│       └── pituitary/
└── requirements.txt       # Python dependencies
```

## 🧠 Model Information

### ResNet-50 Architecture
- **Input Size**: 128x128 pixels
- **Classes**: 4 (Pituitary, Glioma, Meningioma, No Tumor)
- **Training Data**: 5,700+ MRI images
- **Accuracy**: High accuracy on medical imaging datasets

### Tumor Types Detected

#### 1. Pituitary Tumor
- **Description**: Tumors forming in the pituitary gland
- **Cell Structure**: Uniform, small round cells with regular nuclei
- **Severity**: Moderate
- **Survival Rate**: 85-95% with proper treatment

#### 2. Glioma
- **Description**: Tumors arising from glial cells in brain/spinal cord
- **Cell Structure**: Irregular, pleomorphic cells with hyperchromatic nuclei
- **Severity**: High
- **Survival Rate**: Varies by grade (20-80%)

#### 3. Meningioma
- **Description**: Tumors on brain/spinal cord membranes
- **Cell Structure**: Whorled patterns of spindle-shaped cells
- **Severity**: Low to Moderate
- **Survival Rate**: 90-95% with treatment

#### 4. No Tumor
- **Description**: Normal brain tissue
- **Cell Structure**: Regular cellular architecture
- **Severity**: None
- **Treatment**: No treatment required

## 🔬 Analysis Features

### Image Processing
- **Intensity Analysis**: Mean and standard deviation calculations
- **Edge Detection**: Canny edge detection for boundary analysis
- **Texture Analysis**: Local variance measurements
- **Contour Analysis**: Shape and structure evaluation

### Medical Reporting
- **Comprehensive Descriptions**: Detailed medical explanations
- **Symptom Lists**: Common symptoms for each tumor type
- **Treatment Options**: Current medical treatment recommendations
- **Prevention Strategies**: Lifestyle and medical prevention measures
- **Risk Assessment**: Severity levels and survival statistics

## 🎨 Interface Design

### Modern UI Elements
- **Dark Theme**: Professional medical application aesthetic
- **Purple/Blue Gradients**: Modern tech-inspired color scheme
- **Animated Elements**: Smooth transitions and hover effects
- **Responsive Layout**: Adaptive design for all screen sizes

### User Experience
- **Intuitive Upload**: Simple drag-and-drop or click-to-upload
- **Real-time Feedback**: Immediate visual feedback during analysis
- **Detailed Results**: Comprehensive reports with medical context
- **Professional Presentation**: Clean, medical-grade interface

## 🔧 API Endpoints

### POST /analyze
Upload and analyze an MRI image via API

**Request:**
- Content-Type: multipart/form-data
- Body: image file

**Response:**
```json
{
  "name": "Tumor Type",
  "confidence": 95.5,
  "description": "Medical description",
  "cell_structure": "Microscopic analysis",
  "symptoms": ["symptom1", "symptom2"],
  "treatments": ["treatment1", "treatment2"],
  "prevention": ["prevention1", "prevention2"],
  "severity": "Moderate",
  "survival_rate": "85-95%",
  "image_features": {
    "mean_intensity": 127.5,
    "edge_density": 15.2,
    "contour_count": 45
  },
  "analysis_date": "2024-01-15 14:30:00"
}
```

## 🚀 Usage

1. **Upload Image**: Drag and drop or click to upload an MRI image
2. **Analysis**: The system automatically processes the image using ResNet-50
3. **Results**: View comprehensive analysis including:
   - Tumor detection result
   - Confidence score
   - Image statistics
   - Medical information
   - Treatment recommendations
   - Prevention measures

## 🔒 Security & Privacy

- **Local Processing**: All analysis performed locally
- **No Data Storage**: Images are processed and not permanently stored
- **Secure Uploads**: Temporary file handling with automatic cleanup
- **Medical Compliance**: Designed with medical data privacy in mind

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This application is for educational and research purposes. It should not be used as a substitute for professional medical diagnosis. Always consult with qualified healthcare professionals for medical decisions.

## 🆘 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ using Flask, TensorFlow, and modern web technologies**