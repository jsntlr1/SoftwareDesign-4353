from flask import Blueprint, request, jsonify
from db import get_db_connection
from datetime import datetime

event_bp = Blueprint('event', __name__)

@event_bp.route('/events', methods=['POST'])
def create_event():
    try:
        data = request.get_json()
        event_name = data.get('eventName')
        event_description = data.get('eventDescription')
        location = data.get('location')
        required_skills = data.get('requiredSkills')
        urgency = data.get('urgency')
        event_date_str = data.get('eventDate')

        if not all([event_name, event_description, location, required_skills, urgency, event_date_str]):
            return jsonify({'message': 'Missing required fields in event form'}), 400
        
        if not isinstance(required_skills, list):
            return jsonify({'message': 'Required skills must be a list'}), 400

        try:
            event_date = datetime.fromisoformat(event_date_str.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'message': 'Invalid date format'}), 400


        conn = get_db_connection()
        cur = conn.cursor()

        query = """
        INSERT INTO events (name, description, location, required_skills, urgency, date) 
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
        """

        cur.execute(query, (event_name, event_description, location, required_skills, urgency, event_date))
        event_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Event created successfully'}), 201
    except Exception as e:
        print(f'Error creating event: {e}')
        return jsonify({'message': 'ERROR while creating event'}), 500
    


@event_bp.route('/events', methods=['GET'])
def get_events():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
        SELECT id, name, description, location, required_skills, urgency, date
        FROM events;
        """
        cur.execute(query)
        events = cur.fetchall()

        event_list = []
        for event in events:
            event_list.append({
                'id': event[0],
                'name': event[1],
                'description': event[2],
                'location': event[3],
                'requiredSkills': event[4],
                'urgency': event[5],
                'date': event[6].isoformat() if event[6] else None
            })

        cur.close()
        conn.close()


        return jsonify(event_list), 200

    except Exception as e:
        print(f"Error fetching events: {e}")
        return jsonify({"message": "An error occurred while fetching events"}), 500

def find_event(name):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
        SELECT id, name, description, location, required_skills, urgency, date
        FROM events
        WHERE name = %s;
        """
        cur.execute(query, (name,))
        event = cur.fetchone()

        cur.close()
        conn.close()

        if event:
            return {
                'id': event[0],
                'name': event[1],
                'description': event[2],
                'location': event[3],
                'requiredSkills': event[4],
                'urgency': event[5],
                'date': event[6].isoformat() if event[6] else None
            }
        else:
            return None

    except Exception as e:
        print(f"Error finding event: {e}")
        return None