from flask import Blueprint, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from db import get_db_connection
import logging
import datetime

pdf_bp = Blueprint('pdf', __name__)

def generate_pdf(events):
    pdf_output = BytesIO()  
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter


    c.setFont("Helvetica-Bold", 16)
    c.drawString(width / 2 - 50, height - 40, "Event Report")


    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 80, "ID")
    c.drawString(100, height - 80, "Name")
    c.drawString(200, height - 80, "Description")
    c.drawString(350, height - 80, "Location")
    c.drawString(450, height - 80, "Required Skills")
    c.drawString(550, height - 80, "Urgency")
    c.drawString(650, height - 80, "Date")

    c.setFont("Helvetica", 10)
    y_position = height - 100
    
    for event in events:
        event_id = str(event[0]) if event[0] is not None else ""
        name = str(event[1]) if event[1] is not None else ""
        description = str(event[2]) if event[2] is not None else ""
        location = str(event[3]) if event[3] is not None else ""
        required_skills = ', '.join(event[4]) if event[4] is not None else ""
        urgency = str(event[5]) if event[5] is not None else ""
        date = event[6].strftime("%Y-%m-%d") if event[6] is not None else ""

        c.drawString(50, y_position, event_id)
        c.drawString(100, y_position, name)
        c.drawString(200, y_position, description)
        c.drawString(350, y_position, location)
        c.drawString(450, y_position, required_skills)
        c.drawString(550, y_position, urgency)
        c.drawString(650, y_position, date)
        
        y_position -= 20  
        
        if y_position < 60:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 40

    c.save()
    pdf_output.seek(0)
    return pdf_output

def generate_volunteer_pdf(volunteers):
    pdf_output = BytesIO()  
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.drawString(width / 2 - 75, height - 40, "Volunteer Report")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, height - 80, "ID")
    c.drawString(100, height - 80, "Name")
    c.drawString(200, height - 80, "Address1")
    c.drawString(300, height - 80, "Address2")
    c.drawString(400, height - 80, "City")
    c.drawString(500, height - 80, "State")
    c.drawString(550, height - 80, "Zip Code")
    c.drawString(650, height - 80, "Preferences")
    c.drawString(750, height - 80, "Availability")
    c.drawString(850, height - 80, "Skills")

    c.setFont("Helvetica", 10)
    y_position = height - 100
    
    for volunteer in volunteers:
        volunteer_id = str(volunteer[0]) if volunteer[0] is not None else ""
        name = str(volunteer[1]) if volunteer[1] is not None else ""
        address1 = str(volunteer[2]) if volunteer[2] is not None else ""
        address2 = str(volunteer[3]) if volunteer[3] is not None else ""
        city = str(volunteer[4]) if volunteer[4] is not None else ""
        state = str(volunteer[5]) if volunteer[5] is not None else ""
        zip_code = str(volunteer[6]) if volunteer[6] is not None else ""
        preferences = str(volunteer[7]) if volunteer[7] is not None else ""
        availability = ', '.join([a.strftime("%Y-%m-%d") if isinstance(a, datetime.date) else str(a) for a in volunteer[8]]) if volunteer[8] is not None else ""
        skills = ', '.join([str(s) for s in volunteer[9]]) if volunteer[9] is not None else ""

        c.drawString(50, y_position, volunteer_id)
        c.drawString(100, y_position, name)
        c.drawString(200, y_position, address1)
        c.drawString(300, y_position, address2)
        c.drawString(400, y_position, city)
        c.drawString(500, y_position, state)
        c.drawString(550, y_position, zip_code)
        c.drawString(650, y_position, preferences)
        c.drawString(750, y_position, availability)
        c.drawString(850, y_position, skills)
        
        y_position -= 20  
        
        if y_position < 60:
            c.showPage()
            c.setFont("Helvetica", 10)
            y_position = height - 40

    c.save()
    pdf_output.seek(0)
    return pdf_output

@pdf_bp.route('/generate-event-report', methods=['GET'])
def generate_event_report():

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM events ORDER BY date ASC")
        events = cursor.fetchall()
        
        cursor.close()
        conn.close()

        pdf_output = generate_pdf(events)
        
        return send_file(
            pdf_output,
            as_attachment=True,
            download_name="event_report.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        logging.error(f"Error generating PDF report: {e}")
        return {"error": "Failed to generate PDF report"}, 500
    
@pdf_bp.route('/generate-volunteer-report', methods=['GET'])
def generate_volunteer_report():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM volunteers")
        volunteers = cursor.fetchall()
        
        cursor.close()
        conn.close()

        pdf_output = generate_volunteer_pdf(volunteers)
        
        return send_file(
            pdf_output,
            as_attachment=True,
            download_name="volunteer_report.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        logging.error(f"Error generating volunteer PDF report: {e}")
        return {"error": "Failed to generate volunteer PDF report"}, 500