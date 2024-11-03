from flask import Blueprint, request, jsonify
import psycopg2
from db import get_db_connection

event_bp = Blueprint('event', __name__)

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