from flask import jsonify, request, Blueprint
from datetime import datetime
from .models import SerialNumberRecord, SnStatus
from .extensions import db
from marshmallow import Schema, fields, validate, ValidationError
from sqlalchemy.exc import IntegrityError

# Define a blueprint
crud = Blueprint('crud', __name__)

# Marshmallow schema for validation and serialization
class SerialNumberRecordSchema(Schema):
    id = fields.Int(dump_only=True)
    
    # OCR-related fields
    ocr_detected_text = fields.Str(required=True)
    image_file_name = fields.Str()
    image_channels = fields.Int()
    image_format = fields.Str()
    image_height = fields.Int()
    image_size_bytes = fields.Int()
    image_width = fields.Int()
    ocr_language = fields.Str()
    serial_number_extracted = fields.Str()
    ocr_timestamp = fields.DateTime(missing=lambda: datetime.utcnow())
    uploaded_by = fields.Str()
    ocr_status = fields.Str(
        validate=validate.OneOf(["pending", "confirmed", "failed"]),
        missing="pending"
    )
    is_ocr_corrected = fields.Bool(missing=False)
    verified_sn = fields.Str(required=True)

    # Batch information fields
    batch_id = fields.Str()
    batch_quantity = fields.Int()
    batch_item_no = fields.Str()
    part_id = fields.Str(required=True)

    # Testing-related fields
    testing_selected = fields.Bool(missing=False)
    testing_passed = fields.Bool()
    testing_notes = fields.Str()
    testing_user = fields.Str()
    testing_timestamp = fields.DateTime()

    # Serial number recording fields
    recorded_sn = fields.Bool(missing=False)
    recorded_sn_timestamp = fields.DateTime()
    recorded_sn_user = fields.Str()

    # Serial number status (foreign key)
    sn_status_id = fields.Int()

    # Voiding-related fields
    voided = fields.Bool(missing=False)
    voided_timestamp = fields.DateTime()
    voided_user = fields.Str()

    # Soft delete field
    is_deleted = fields.Bool(dump_only=True)

    class Meta:
        ordered = True

# Instantiate schemas
serial_number_schema = SerialNumberRecordSchema()
serial_numbers_schema = SerialNumberRecordSchema(many=True)

# Create a new serial number record
@crud.route('/serial_number', methods=['POST'])
def create_serial_number():
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        # Validate and deserialize input
        data = serial_number_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        new_record = SerialNumberRecord(**data)
        db.session.add(new_record)
        db.session.commit()
        result = serial_number_schema.dump(new_record)
        return jsonify({"message": "Serial number record created", "data": result}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

# Update an existing serial number record
@crud.route('/serial_number/<int:id>', methods=['PUT'])
def update_serial_number(id):
    json_data = request.get_json()
    if not json_data:
        return jsonify({"error": "No input data provided"}), 400

    record = SerialNumberRecord.query.get_or_404(id)

    try:
        # Validate and deserialize input
        data = serial_number_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        for key, value in data.items():
            setattr(record, key, value)
        db.session.commit()
        result = serial_number_schema.dump(record)
        return jsonify({"message": "Serial number record updated", "data": result}), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

# Void a serial number record
@crud.route('/serial_number/<int:id>/void', methods=['PATCH'])
def void_serial_number(id):
    record = SerialNumberRecord.query.get_or_404(id)
    json_data = request.get_json() or {}

    if record.voided:
        return jsonify({"error": "Record is already voided"}), 409

    try:
        record.voided = True
        record.voided_timestamp = datetime.utcnow()
        record.voided_user = json_data.get('voided_user', 'unknown')
        db.session.commit()
        result = serial_number_schema.dump(record)
        return jsonify({"message": "Serial number record voided", "data": result}), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

# Query serial number records with filters and pagination
@crud.route('/serial_numbers/query', methods=['GET'])
def query_serial_numbers():
    # Get query parameters
    start_date = request.args.get('start_date')  # Expected format: YYYY-MM-DD
    end_date = request.args.get('end_date')      # Expected format: YYYY-MM-DD
    batch_id = request.args.get('batch_id')
    serial_number_min = request.args.get('serial_number_min')
    serial_number_max = request.args.get('serial_number_max')
    user = request.args.get('user')
    voided = request.args.get('voided')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)

    # Base query excluding soft-deleted records
    query = SerialNumberRecord.query.filter_by(is_deleted=False)

    try:
        # Filter by start date
        if start_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
                query = query.filter(SerialNumberRecord.ocr_timestamp >= start_date_obj)
            except ValueError:
                return jsonify({"error": "Invalid start_date format. Expected YYYY-MM-DD."}), 400

        # Filter by end date
        if end_date:
            try:
                end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
                query = query.filter(SerialNumberRecord.ocr_timestamp <= end_date_obj)
            except ValueError:
                return jsonify({"error": "Invalid end_date format. Expected YYYY-MM-DD."}), 400

        # Filter by batch ID
        if batch_id:
            query = query.filter(SerialNumberRecord.batch_id == batch_id)

        # Filter by serial number range
        if serial_number_min and serial_number_max:
            query = query.filter(
                SerialNumberRecord.serial_number_extracted.between(serial_number_min, serial_number_max)
            )
        elif serial_number_min:
            query = query.filter(SerialNumberRecord.serial_number_extracted >= serial_number_min)
        elif serial_number_max:
            query = query.filter(SerialNumberRecord.serial_number_extracted <= serial_number_max)

        # Filter by user
        if user:
            query = query.filter(SerialNumberRecord.uploaded_by == user)

        # Filter by voided status
        if voided is not None:
            if voided.lower() == 'true':
                query = query.filter(SerialNumberRecord.voided == True)
            elif voided.lower() == 'false':
                query = query.filter(SerialNumberRecord.voided == False)
            else:
                return jsonify({"error": "Invalid voided parameter. Expected 'true' or 'false'."}), 400

        # Apply pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        serial_numbers = pagination.items

        # Serialize results
        result = serial_numbers_schema.dump(serial_numbers)

        return jsonify({
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "per_page": pagination.per_page,
            "data": result
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@crud.route('/serial_number/<int:id>', methods=['DELETE'])
def delete_serial_number(id):
    record = SerialNumberRecord.query.get_or_404(id)

    try:
        # Soft delete by setting is_deleted to True
        record.is_deleted = True
        db.session.commit()
        return jsonify({"message": "Serial number record soft deleted", "id": record.id}), 200

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database integrity error", "details": str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
