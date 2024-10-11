from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .extensions import db

class SerialNumberRecord(db.Model):
    # Information from the OCR system
    id = db.Column(db.Integer, primary_key=True)
    ocr_detected_text = db.Column(db.Text)
    image_file_name = db.Column(db.String(255))
    image_channels = db.Column(db.Integer)
    image_format = db.Column(db.String(50))
    image_height = db.Column(db.Integer)
    image_size_bytes = db.Column(db.BigInteger)
    image_width = db.Column(db.Integer)
    ocr_language = db.Column(db.String(10))
    serial_number_extracted = db.Column(db.String(255))
    ocr_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    uploaded_by = db.Column(db.String(50))
    ocr_status = db.Column(db.String(50))
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Did the OCR system detect the serial number correctly?
    is_ocr_corrected = db.Column(db.Boolean, default=False)
    verified_sn = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    # Information about the batch and item in the batch
    batch_id = db.Column(db.String(50))  # work order / receiving documents
    batch_quantity = db.Column(db.Integer)  # total quantity of items in the batch
    batch_item_no = db.Column(db.Integer)  # item number in the batch
    part_id = db.Column(db.String(50), nullable=False)  # item 
    batch_type = db.Column(db.String(50))  # work order / receiving documents
    batch_description = db.Column(db.Text)  # work order / receiving documents

    # Item Selected for testing
    testing_selected = db.Column(db.Boolean, default=False)
    testing_passed = db.Column(db.Boolean, default=False)
    testing_notes = db.Column(db.Text)
    testing_user = db.Column(db.String(50))
    testing_timestamp = db.Column(db.DateTime)

    # Was the serial number recorded
    recorded_sn = db.Column(db.Boolean, default=False)
    recorded_sn_timestamp = db.Column(db.DateTime)
    recorded_sn_user = db.Column(db.String(50))

    # Serial Number Status (foreign key to SnStatus table)
    sn_status_id = db.Column(db.Integer, db.ForeignKey('sn_status.id'), nullable=False)
    
    # Relationship to sn_status table
    sn_status = db.relationship('SnStatus', backref='serial_numbers')

    # Voided
    voided = db.Column(db.Boolean, default=False)
    voided_timestamp = db.Column(db.DateTime)
    voided_user = db.Column(db.String(50))

class SnStatus(db.Model):  # Renamed for Python class naming convention
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)





