from flask import Blueprint, request, jsonify
from event_management import find_event
import psycopg2
from db import get_db_connection

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
    volunteer_name = data.get('volunteerName')
    event_name = data.get('matchedEvent')

    if not volunteer_name or not event_name:
        return jsonify({"message" : "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT id FROM volunteers WHERE name = %s;", (volunteer_name,))
        volunteer = cur.fetchone()
        if not volunteer:
            cur.close()
            conn.close()
            return jsonify({"message": "Volunteer not found"}), 400
        volunteer_id = volunteer[0]

        cur.execute("SELECT id FROM events WHERE name = %s;", (event_name,))
        event = cur.fetchone()
        if not event:
            cur.close()
            conn.close()
            return jsonify({"message": "Event not found"}), 400
        event_id = event[0]

        cur.execute("INSERT INTO volunteer_history (volunteer_id, event_id) VALUES (%s, %s) RETURNING id;", (volunteer_id, event_id))
        match_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Volunteer matched successfully", "match_id": match_id}), 201
    except Exception as e:
        return jsonify({"message": "ERROR while matching volunteers"}), 500
    

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
