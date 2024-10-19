from flask import Flask
from flask_cors import CORS
from event_management import event_bp
from volunteer_matching import volunteer_bp

app = Flask(__name__, static_folder='../frontend/dist')
CORS(app)

app.register_blueprint(event_bp, url_prefix='/api')
app.register_blueprint(volunteer_bp, url_prefix='/api')

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
    
    app.run(debug=True)
