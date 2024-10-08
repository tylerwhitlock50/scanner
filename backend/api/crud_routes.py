from flask import jsonify, request, Blueprint
from .models import SerialNumberRecord, SnStatus
from datetime import datetime
from .extensions import db

# Define a blueprint
crud = Blueprint('crud', __name__)

@crud.route('/serial_number', methods=['POST'])
def create_serial_number():
    data = request.json

    try:
        new_record = SerialNumberRecord(
            # OCR-related fields
            ocr_detected_text=data.get('ocr_detected_text'),
            image_file_name=data.get('image_file_name'),
            image_channels=data.get('image_metadata', {}).get('image_channels'),
            image_format=data.get('image_metadata', {}).get('image_format'),
            image_height=data.get('image_metadata', {}).get('image_height'),
            image_size_bytes=data.get('image_metadata', {}).get('image_size_bytes'),
            image_width=data.get('image_metadata', {}).get('image_width'),
            ocr_language=data.get('ocr_language'),
            serial_number_extracted=data.get('serial_number_extracted'),
            ocr_timestamp=data.get('ocr_timestamp', datetime.utcnow()),
            uploaded_by=data.get('uploaded_by'),
            ocr_status=data.get('ocr_status','pending'),
            is_ocr_corrected=data.get('is_ocr_corrected', False),  # Default to False
            verified_sn=data.get('verified_sn'),  # This is required, so it must be present

            # Batch information fields
            batch_id=data.get('batch_id'),
            batch_quantity=data.get('batch_quantity'),
            batch_item_no=data.get('batch_item_no'),

            # Testing-related fields
            testing_selected=data.get('testing_selected', False),
            testing_passed=data.get('testing_passed', False),
            testing_notes=data.get('testing_notes'),
            testing_user=data.get('testing_user'),
            testing_timestamp=data.get('testing_timestamp'),

            # Serial number recording fields
            recorded_sn=data.get('recorded_sn', False),
            recorded_sn_timestamp=data.get('recorded_sn_timestamp'),
            recorded_sn_user=data.get('recorded_sn_user'),

            # Serial number status (foreign key)
            sn_status_id=data.get('sn_status_id'),

            # Voiding-related fields
            voided=data.get('voided', False),
            voided_timestamp=data.get('voided_timestamp'),
            voided_user=data.get('voided_user')
        )

        db.session.add(new_record)
        db.session.commit()
        
        return jsonify({"message": "Serial number record created", "id": new_record.id}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@crud.route('/serial_number/<int:id>', methods=['PUT'])
def update_serial_number(id):
    data = request.json
    record = SerialNumberRecord.query.get_or_404(id)

    try:
        # Update only fields provided in the request
        record.ocr_detected_text = data.get('ocr_detected_text', record.ocr_detected_text)
        record.image_file_name = data.get('image_file_name', record.image_file_name)
        record.image_channels = data.get('image_metadata', {}).get('image_channels', record.image_channels)
        record.image_format = data.get('image_metadata', {}).get('image_format', record.image_format)
        record.image_height = data.get('image_metadata', {}).get('image_height', record.image_height)
        record.image_size_bytes = data.get('image_metadata', {}).get('image_size_bytes', record.image_size_bytes)
        record.image_width = data.get('image_metadata', {}).get('image_width', record.image_width)
        record.ocr_language = data.get('ocr_language', record.ocr_language)
        record.serial_number_extracted = data.get('serial_number_extracted', record.serial_number_extracted)
        record.ocr_timestamp = data.get('ocr_timestamp', record.ocr_timestamp)
        record.uploaded_by = data.get('uploaded_by', record.uploaded_by)
        record.ocr_status = data.get('ocr_status', record.ocr_status)
        record.is_ocr_corrected = data.get('is_ocr_corrected', record.is_ocr_corrected)
        record.verified_sn = data.get('verified_sn', record.verified_sn)

        # Update batch fields
        record.batch_id = data.get('batch_id', record.batch_id)
        record.batch_quantity = data.get('batch_quantity', record.batch_quantity)
        record.batch_item_no = data.get('batch_item_no', record.batch_item_no)

        # Update testing fields
        record.testing_selected = data.get('testing_selected', record.testing_selected)
        record.testing_passed = data.get('testing_passed', record.testing_passed)
        record.testing_notes = data.get('testing_notes', record.testing_notes)
        record.testing_user = data.get('testing_user', record.testing_user)
        record.testing_timestamp = data.get('testing_timestamp', record.testing_timestamp)

        # Update recording fields
        record.recorded_sn = data.get('recorded_sn', record.recorded_sn)
        record.recorded_sn_timestamp = data.get('recorded_sn_timestamp', record.recorded_sn_timestamp)
        record.recorded_sn_user = data.get('recorded_sn_user', record.recorded_sn_user)

        # Update serial number status
        record.sn_status_id = data.get('sn_status_id', record.sn_status_id)

        # Update voiding fields
        record.voided = data.get('voided', record.voided)
        record.voided_timestamp = data.get('voided_timestamp', record.voided_timestamp)
        record.voided_user = data.get('voided_user', record.voided_user)

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Serial number record updated", "id": record.id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@crud.route('/serial_number/<int:id>/void', methods=['PUT'])
def void_serial_number(id):
    record = SerialNumberRecord.query.get_or_404(id)

    # Check if the record is already voided
    if record.voided:
        return jsonify({"message": "Record is already voided"}), 400

    try:
        # Void the record by setting the voided flag to True
        record.voided = True
        record.voided_timestamp = datetime.utcnow()  # Set the voided timestamp
        record.voided_user = request.json.get('voided_user', 'unknown')  # Track who voided the record

        # Commit the change to the database
        db.session.commit()

        return jsonify({"message": "Serial number record voided", "id": record.id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@crud.route('/serial_number/<int:id>', methods=['DELETE'])
def delete_serial_number(id):
    # Fetch the record by ID, return 404 if not found
    record = SerialNumberRecord.query.get_or_404(id)

    try:
        # Delete the record from the database
        db.session.delete(record)
        db.session.commit()

        return jsonify({"message": "Serial number record deleted", "id": record.id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@crud.route('/serial_numbers/query', methods=['GET'])
def query_serial_numbers():
    # Get query parameters from the request
    start_date = request.args.get('start_date')  # YYYY-MM-DD format
    end_date = request.args.get('end_date')  # YYYY-MM-DD format
    batch_id = request.args.get('batch_id')
    serial_number_min = request.args.get('serial_number_min')
    serial_number_max = request.args.get('serial_number_max')
    user = request.args.get('user')
    voided = request.args.get('voided')

    # Base query
    query = SerialNumberRecord.query

    try:
        # Filter by start and end dates (ocr_timestamp)
        if start_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(SerialNumberRecord.ocr_timestamp >= start_date_obj)

        if end_date:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(SerialNumberRecord.ocr_timestamp <= end_date_obj)

        # Filter by batch_id
        if batch_id:
            query = query.filter(SerialNumberRecord.batch_id == batch_id)

        # Filter by serial number range
        if serial_number_min and serial_number_max:
            query = query.filter(SerialNumberRecord.serial_number_extracted.between(serial_number_min, serial_number_max))
        elif serial_number_min:
            query = query.filter(SerialNumberRecord.serial_number_extracted >= serial_number_min)
        elif serial_number_max:
            query = query.filter(SerialNumberRecord.serial_number_extracted <= serial_number_max)

        if user:
            query = query.filter(SerialNumberRecord.uploaded_by == user)

        if voided:
            query = query.filter(SerialNumberRecord.voided == (voided.lower() == 'true'))

        # Execute query and fetch results
        serial_numbers = query.all()

        # Convert results to a list of dictionaries
        results = [{
            "id": record.id,
            "ocr_detected_text": record.ocr_detected_text,
            "serial_number_extracted": record.serial_number_extracted,
            "ocr_timestamp": record.ocr_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "batch_id": record.batch_id,
            "voided": record.voided,
            "sn_status": record.sn_status.status
        } for record in serial_numbers]

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400