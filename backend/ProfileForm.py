from flask import Flask, request, jsonify, Blueprint
import logging
from db import get_db_connection


logging.basicConfig(level=logging.INFO)
profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods = ['POST'])
def create_volunteer_profile():
    data = request.get_json()
    try:
        full_name = data.get('fullName')
        address1 = data.get('address1')
        address2 = data.get('address2')
        city = data.get('city')
        state = data.get('state')
        zip_code = data.get('zipCode')
        preferences = data.get('preferences')
        availability = data.get('availability')
        skills = data.get('skills')

        if not full_name or not address1 or not city or not state or not zip_code or not skills:
            return jsonify({'error:' 'Missing required fields in profile'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()

        insert_volunteer_sql = """
        INSERT INTO volunteers (name, address1, address2, city, state, zip_code, preferences, availability, skills)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s::date[], %s::text[])
        RETURNING id;
        """

        cur.execute(insert_volunteer_sql, (full_name, address1, address2, city, state, zip_code,preferences, availability, skills))
        volunteer_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Volunteer profile successfully created', 'volunteer_id': volunteer_id}), 201
    
    except Exception as e:
        logging.error(f"Error creating volunteer from profile: {e}")
        return jsonify({'error': 'ERROR while creating volunteer profile'})