from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
#placeholder before database implementation
profiles = {}

@app.route('/api/profile', methods = ['POST', 'OPTIONS'])
def receive_profile():
    if request.method == 'OPTIONS':
        response = jsonify({'message': 'CORS preflight'})
        response.status_code = 200
        return response
    elif request.method == 'POST':
        data = request.get_json()
        print("Received profile data:", data)
        user_id = "user_1"
        profiles[user_id] = data;
        return jsonify({'message': 'Profile data received successfully'}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Flask server is running'}), 200

if __name__ == '__main__':
    app.run(debug=True)

