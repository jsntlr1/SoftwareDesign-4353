from flask import Blueprint, request, jsonify
from event_management import find_event
from db import get_db_connection
from datetime import datetime

volunteer_bp = Blueprint('volunteer', __name__)

@volunteer_bp.route('/volunteers', methods=['GET'])
def get_volunteers():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, name, skills FROM volunteers;")
        volunteers = cur.fetchall()

        volunteer_list = []
        for volunteer in volunteers:
            volunteer_list.append({
                'id': volunteer[0],
                'name': volunteer[1],
                'skills': volunteer[2]
            })
        
        cur.close()
        conn.close()

        return jsonify(volunteer_list), 200
    except Exception as e:
        return jsonify({'error': 'ERROR while fetching volunteers'}), 500
    
@volunteer_bp.route('/match', methods=['POST'])
def match_volunteer():
    data = request.get_json()
    volunteer_id = data.get('volunteerId')
    event_id = data.get('eventId')

    if not volunteer_id or not event_id:
        return jsonify({"message" : "Missing volunteer or event ids"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM volunteers WHERE id = %s;", (volunteer_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"message": "Volunteer not found"}), 400

        cur.execute("SELECT id, date FROM events WHERE id = %s;", (event_id,))
        event_row = cur.fetchone()
        print(f"event_row: {event_row}")
        if not event_row:
            cur.close()
            conn.close()
            return jsonify({"message": "Event not found"}), 404
        event_date = event_row[1]

        if isinstance(event_date, datetime):
            event_date = event_date.date()
        elif isinstance(event_date, str):
            event_date = datetime.strptime(event_date, '%Y-%m-%d').date()

        
        cur.execute("SELECT id FROM volunteer_history WHERE volunteer_id = %s AND event_id = %s;", (volunteer_id, event_id))
        existing_registration = cur.fetchone()
        if existing_registration:
            cur.close()
            conn.close()
            return jsonify({'message': 'You have already registered for this event'}), 400

        cur.execute("INSERT INTO volunteer_history (volunteer_id, event_id, participation_date) VALUES (%s, %s, %s) RETURNING id;", (volunteer_id, event_id, event_date))
        match_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Successfully registered for event", "match_id": match_id}), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error registering volunteer: {e}")
        return jsonify({"message": "ERROR while matching volunteers"}), 500



@volunteer_bp.route('/available_events', methods=['POST'])
def get_available_events():
    data = request.get_json()
    volunteer_name = data.get('volunteerName')

    if not volunteer_name:
        return jsonify({'message': 'Volunteer name not found'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id, availability FROM volunteers WHERE name = %s", (volunteer_name,))
        volunteer = cur.fetchone()
        if not volunteer:
            cur.close()
            conn.close()
            return jsonify({'message': 'volunteer not found'}), 404
        volunteer_id = volunteer[0]
        availability_dates = volunteer[1]
        if not availability_dates:
            cur.close()
            conn.close()
            return jsonify({'message': 'Not availability dates found for volunteer'}), 404
        
        cur.execute("""
                    SELECT id, name, description, location, date
                    FROM events
                    WHERE date = ANY(%s)""", (availability_dates,))
        events = cur.fetchall()

        event_list = []
        for event in events:
            event_list.append({
                'id': event[0],
                'name': event[1],
                'description': event[2],
                'location': event[3],
                'date': event[4].isoformat() if event[4] else None
            })
        
        cur.close()
        conn.close()
        return jsonify({'volunteerId': volunteer_id, 'events': event_list}), 200
    except Exception as e:
        print(f"Error getting available events: {e}")
        return jsonify({"message": "Error while getting available events"}), 500

@volunteer_bp.route('/match', methods=['GET'])
def get_matches():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT vh.id, v.name AS volunteer_name, e.name as event_name, vh.participation_date
            FROM volunteer_history vh
            JOIN volunteers v on vh.volunteer_id = v.id
            JOIN events e ON vh.event_id = e.id;
            """
            )
        matches = cur.fetchall()

        match_list = []
        for match in matches:
            match_list.append({
                'id': match[0],
                'volunteer_name': match[1],
                'event_name': match[2],
                'participation_date': match[3].isoformat()
            })
        
        cur.close()
        conn.close()

        return jsonify(match_list), 200
    except Exception as e:
        return jsonify({"message": "ERROR while fetching event matches"})
    

@volunteer_bp.route('/eventhistory')
def eventHistory():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user ID'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
        SELECT e.id, e.name, e.description, e.location, e.date
        FROM events e
        JOIN volunteer_history vh ON e.id = vh.event_id
        WHERE vh.volunteer_id = %s;
        """

        cur.execute(query, (user_id,))
        events = cur.fetchall()

        data = []
        for event in events:
            data.append({
                'id': event[0],
                'name': event[1],
                'description': event[2],
                'location': event[3],
                'date': event[4].isoformat() if event[4] else None
            })

        cur.close()
        conn.close()
        return jsonify(data), 200

    except Exception as e:
        return jsonify({'error': 'ERROR while fetching event history'}), 500
