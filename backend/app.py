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



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return "Login page"
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return jsonify({"credentials": "received"})
        
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
