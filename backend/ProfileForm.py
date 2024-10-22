from flask import Flask, request, jsonify, Blueprint
import logging

logging.basicConfig(level=logging.INFO)
profile_bp = Blueprint('profile', __name__)

#placeholder before database implementation
profiles = {}

@profile_bp.route('/profile', methods = ['POST'])
def receive_profile():
    data = request.get_json()
    if not data:
        return jsonify({'ERROR: no data found'}), 400

    logging.info(f"Received profile data: {data}")
    user_id = data.get('user_id', 'default_user')
    profiles[user_id] = data

    return jsonify({'messsage': 'Profile data received successfully'}), 201


