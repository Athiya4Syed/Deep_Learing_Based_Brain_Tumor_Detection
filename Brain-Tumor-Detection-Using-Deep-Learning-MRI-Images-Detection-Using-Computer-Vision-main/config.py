"""
Configuration file for Brain Tumor Detection Application
"""

import os

# Gemini AI Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-gemini-api-key-here')

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Database Configuration (if using PostgreSQL)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///brain_tumor.db')

# Application Configuration
DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
HOST = os.getenv('FLASK_HOST', '127.0.0.1')
PORT = int(os.getenv('FLASK_PORT', 5000))

# File Upload Configuration
UPLOAD_FOLDER = './uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Model Configuration
MODEL_PATH = './models/model.h5'
IMAGE_SIZE = 128

# Chatbot Configuration
CHATBOT_MAX_HISTORY = 10
CHATBOT_TIMEOUT = 30  # seconds

