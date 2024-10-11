import os
import io
import cv2
from flask import Blueprint, request, jsonify, render_template
from google.cloud import vision
from google.cloud.vision_v1 import types
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np
import re
from datetime import datetime

# Define a blueprint
ocr = Blueprint('ocr', __name__)

# Set Google Cloud Vision client
client = vision.ImageAnnotatorClient()

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check allowed file type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def isolate_serial_number(text):
    """
    Extracts the serial number from the given text.

    Prioritizes finding patterns with "S.N." followed by numbers, 
    but falls back to extracting any sequence of digits if no "S.N." pattern is found.
    """

    # First, try to find the "S.N." pattern followed by 7 digits
    sn_pattern = r'(?:S/N|SN|S\.N\.)\s*(\d{7})'  # Matches "S.N." with any number of spaces and then 7 digits
    match = re.search(sn_pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)  # Return the captured group (the 7 digits)

    # If the above pattern is not found, look for any 7-digit number
    fallback_pattern = r'(\d{7})' 
    match = re.search(fallback_pattern, text)
    if match:
        return match.group(1) 

    # If no serial number is found, return None (or an appropriate message)
    return 'None'  


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
@ocr.route('/')
def index():
    return render_template('index.html')

@ocr.route('/upload', methods=['POST'])
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

        # Isolate the serial number from the detected text
        serial_number = isolate_serial_number(detected_text)

        confidence_scores = []
        if response.full_text_annotation:
            for page in response.full_text_annotation.pages:
                for block in page.blocks:
                    confidence_scores.append(block.confidence)

        data = {
            "ocr_detected_text": detected_text,
            "serial_number_extracted": serial_number,  # Renamed for consistency
            "image_file_name": filename,  # Updated naming convention
            "image_metadata": {
                "image_width": img.shape[1],  # Updated naming convention
                "image_height": img.shape[0],  # Updated naming convention
                "image_channels": img.shape[2],  # Updated naming convention
                "image_size_bytes": len(img_bytes),  # Updated naming convention
                "image_format": file.content_type  # Updated naming convention
            },
            "confidence_scores": confidence_scores,  # Pluralized for clarity
            "ocr_language": texts[0].locale if texts else None,  # Updated naming convention
            "ocr_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Updated naming convention
        }


        return jsonify(data), 200 
