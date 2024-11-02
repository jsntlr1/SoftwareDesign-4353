from flask import Flask, jsonify, request
from flask_cors import CORS
from event_management import event_bp
from volunteer_matching import volunteer_bp
from Notifications import notifications_bp
from ProfileForm import profile_bp


app = Flask(__name__, static_folder='dist')
CORS(app)

app.register_blueprint(event_bp, url_prefix='/api')
app.register_blueprint(volunteer_bp, url_prefix='/api')
app.register_blueprint(notifications_bp, url_prefix='/api')
app.register_blueprint(profile_bp, url_prefix='/api')

conn = psycopg2.connect(
        database="designproject",
        user="postgres",
        password="thechef",
        host="localhost",
        port="5432"
    )
cursor = conn.cursor()
cursor.execute(
        '''CREATE TABLE IF NOT EXISTS usercredentials (id varchar(100) PRIMARY KEY, password varchar(60));'''
    )
cursor.execute(
        '''CREATE TABLE IF NOT EXISTS userprofile (fname varchar(15), lname varchar(25), address varchar(100), availability time);'''
    )
cursor.close()
conn.close()

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = psycopg2.connect(
        database="database",
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT password FROM usercredentials WHERE username = (%s)''', (username,)
        )
        login_success = 0
        res = cursor.fetchone()
        if (res and res[0] == password):
            login_success = 1
            
        cursor.close()
        conn.close()
        return jsonify({"login": login_success})
        
@app.route('/eventhistory')
def eventHistory():
    userEvents = [] # represents the list of events queried from the database for a particular user
    data = {}
    for i in range(len(userEvents)):
        data[str(i)] = userEvents[i]
    
    return jsonify(data)

@app.route('/')
def home():
    return "Backend server is running"

if __name__ == '__main__':
    from event_management import events
    from volunteer_matching import volunteers
    
    events.append({
        'id': 1,
        'name': 'Community Cleanup',
        'description': 'Help clean up the local park',
        'location': 'Central Park',
        'requiredSkills': ['teamwork', 'physical fitness'],
        'urgency': 'medium',
        'date': '2024-11-15'
    })
    volunteers.append({
        'id': 1,
        'name': 'John Doe',
        'skills': ['communication', 'teamwork']
    })
    
    app.run(debug=True, port=5000)
