from flask import send_file, jsonify, request, Blueprint
import io
from reportlab.lib.pagesizes import letter  # Using letter size for more space
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from barcode.codex import Code128
from barcode.writer import ImageWriter
from PIL import Image
from .models import SerialNumberRecord, BatchInfo
from .crud_routes_v3 import serial_numbers_schema

reports = Blueprint('reports', __name__)

@reports.route('/serial_numbers/report', methods=['GET'])
def generate_report():
    batch_id = str(request.args.get('batch_id'))
    if not batch_id:
        return jsonify({"error": "batch_id is required"}), 400

    try:
        # Query the batch record first to get the batch_info_id
        batch_record = BatchInfo.query.filter_by(batch_number=batch_id).first()

        if not batch_record:
            return jsonify({"message": "Batch not found."}), 404

        # Query for serial numbers associated with the batch using batch_info_id
        records = SerialNumberRecord.query.filter(
            SerialNumberRecord.batch_info_id == batch_record.id,
            SerialNumberRecord.is_deleted == False
        ).all()
        
        data = serial_numbers_schema.dump(records)

        # Prepare a PDF file with letter page size
        output = io.BytesIO()
        pdf = canvas.Canvas(output, pagesize=letter)
        width, height = letter
        pdf.setTitle(f"Batch {batch_id} Report")

        # Desired barcode dimensions in points (2 inches by 1 inch)
        barcode_width = 2 * 72  # 2 inches in points
        barcode_height = 1 * 72  # 1 inch in points

        # Grid configuration: 4 columns, 5 rows per page
        columns = 3
        rows_per_page = 8
        x_margin = 50  # Margin from left
        y_margin = height - 100  # Start margin from the top
        x_spacing = (width - 2 * x_margin - columns * barcode_width) / (columns - 1)
        y_spacing = 50  # Space between rows

        # Track positions in the grid
        column = 0
        row = 0

        for sn in data:
            serial_number = sn['verified_sn']

            # Calculate the position for this barcode
            x_position = x_margin + column * (barcode_width + x_spacing)
            y_position = y_margin - row * (barcode_height + y_spacing)

            # Create barcode image in memory
            barcode = Code128(serial_number, writer=ImageWriter())
            buffer = io.BytesIO()
            barcode.write(buffer)
            buffer.seek(0)
            barcode_image = Image.open(buffer)

            # Convert the barcode image to RGB
            barcode_image = barcode_image.convert("RGB")
            image_buffer = io.BytesIO()
            barcode_image.save(image_buffer, format='PNG')
            image_buffer.seek(0)

            # Use reportlab's image utils to convert the buffer into an image object
            image = utils.ImageReader(image_buffer)

            # Add barcode image to the PDF at the calculated position
            pdf.drawImage(image, x_position, y_position, width=barcode_width, height=barcode_height)

            # Move to the next position in the grid
            column += 1
            if column == columns:
                column = 0
                row += 1

            # If we've filled all rows, start a new page
            if row == rows_per_page:
                pdf.showPage()  # Start a new page
                row = 0
                column = 0

        # Finalize the PDF
        pdf.save()
        output.seek(0)

        # Send the PDF as a downloadable file
        return send_file(output, download_name=f'Batch_{batch_id}_Report.pdf', as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
