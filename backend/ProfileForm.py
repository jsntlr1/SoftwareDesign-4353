from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#placeholder before dictionary implementation
profiles = {}

@app.route('/api/profile', methods = ['POST'])
def receive_profile():
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

