from flask import Blueprint, request, jsonify
from event_management import find_event

volunteer_bp = Blueprint('volunteer', __name__)

volunteers = []
matches = []

@volunteer_bp.route('/volunteers', methods=['POST'])
def create_volunteer():
    data = request.json
    new_volunteer = {
        'id': len(volunteers) + 1,
        'name': data['name'],
        'skills': data['skills']
    }
    volunteers.append(new_volunteer)
    return jsonify({"message": "Volunteer created successfully"}), 201

@volunteer_bp.route('/volunteers', methods=['GET'])
def get_volunteers():
    return jsonify(volunteers)

@volunteer_bp.route('/match', methods=['POST'])
def match_volunteer():
    data = request.json
    volunteer = find_volunteer(data['volunteerName'])
    event = find_event(data['matchedEvent'])
    
    if not volunteer or not event:
        return jsonify({"message": "Volunteer or Event not found"}), 404
    
    new_match = {
        'id': len(matches) + 1,
        'volunteer_id': volunteer['id'],
        'event_id': event['id']
    }
    matches.append(new_match)
    return jsonify({"message": "Volunteer matched successfully"}), 201

@volunteer_bp.route('/match', methods=['GET'])
def get_matches():
    return jsonify(matches)

def find_volunteer(name):
    return next((volunteer for volunteer in volunteers if volunteer['name'] == name), None)