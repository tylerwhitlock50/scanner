import os
import io
import cv2
from flask import Blueprint, request, jsonify, render_template
from google.cloud import vision
from google.cloud.vision_v1 import types
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np

# Define a blueprint
api = Blueprint('main', __name__)

# Set Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check allowed file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    """
    Preprocess the image for better OCR:
    - Convert to grayscale
    - Increase contrast using histogram equalization
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Increase contrast using histogram equalization
    contrast_enhanced = cv2.equalizeHist(gray)

    return contrast_enhanced


# Route to serve the upload form
@api.route('/')
def index():
    return render_template('index.html')

@api.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        img_bytes = file.read()

        # Convert the image bytes into an OpenCV image
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Preprocess the image (greyscale and contrast enhancement)
        processed_img = preprocess_image(img)

        # Convert the processed image back to bytes to send to Google Vision API
        _, buffer = cv2.imencode('.jpg', processed_img)
        processed_img_bytes = buffer.tobytes()

        # Convert the processed image to a format for Google Vision API
        image = vision.Image(content=processed_img_bytes)

        # Call the Google Vision API
        response = client.text_detection(image=image)
        texts = response.text_annotations

        if response.error.message:
            return jsonify({"error": response.error.message}), 500

        # Get the detected text
        detected_text = texts[0].description if texts else ""

        return jsonify({"detected_text": detected_text}), 200

    return jsonify({"error": "Invalid file type"}), 400
