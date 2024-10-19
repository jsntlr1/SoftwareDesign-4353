from flask import Blueprint, request, jsonify

event_bp = Blueprint('event', __name__)

events = []

@event_bp.route('/events', methods=['POST'])
def create_event():
    data = request.json
    new_event = {
        'id': len(events) + 1,
        'name': data['eventName'],
        'description': data['eventDescription'],
        'location': data['location'],
        'requiredSkills': data['requiredSkills'],
        'urgency': data['urgency'],
        'date': data['eventDate']
    }
    events.append(new_event)
    return jsonify({"message": "Event created successfully"}), 201

@event_bp.route('/events', methods=['GET'])
def get_events():
    return jsonify(events)

def find_event(name):
    return next((event for event in events if event['name'] == name), None)