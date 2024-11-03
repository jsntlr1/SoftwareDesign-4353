from flask import Flask, jsonify, request
from flask_cors import CORS
from event_management import event_bp
from volunteer_matching import volunteer_bp
from Notifications import notifications_bp
from ProfileForm import profile_bp
from db import get_db_connection
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__, static_folder='dist')
CORS(app)

app.register_blueprint(event_bp, url_prefix='/api')
app.register_blueprint(volunteer_bp, url_prefix='/api')
app.register_blueprint(notifications_bp, url_prefix='/api')
app.register_blueprint(profile_bp, url_prefix='/api')

def init_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
        '''CREATE TABLE IF NOT EXISTS usercredentials (id varchar(100) PRIMARY KEY, password varchar(60));'''
        )
        
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS volunteers(id SERIAL PRIMARY KEY, name VARCHAR(120), address1 VARCHAR(100), address2 VARCHAR(100), city VARCHAR(100), state VARCHAR(2) REFERENCES states(code), zip_code VARCHAR(9), preferences TEXT, availability DATE[], skills TEXT[]);'''
        )
        
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS volunteer_history(id SERIAL PRIMARY KEY, volunteer_id INTEGER NOT NULL, event_id INTEGER NOT NULL, participation_date DATE DEFAULT CURRENT_DATE, FOREIGN KEY (volunteer_id) REFERENCES volunteers(id), FOREIGN KEY (event_id) REFERENCES events(id));'''
        )

        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS events(id SERIAL PRIMARY KEY, name VARCHAR(120), description TEXT, location VARCHAR(120), required_skills TEXT[], urgency VARCHAR(50), date DATE); '''
        )

        #states located in /backend/sql_statements

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        logging.error("error with db init: %s", e)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    conn = get_db_connection()

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT password FROM usercredentials WHERE id = (%s)''', (username,)
        )
        login_success = 0
        res = cursor.fetchone()
        if (res and res[0] == password):
            login_success = 1
            
        cursor.close()
        conn.close()
        return jsonify({"login": login_success})
        

@app.route('/')
def home():
    return "Backend server is running"

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)