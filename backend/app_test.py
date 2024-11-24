import pytest
from flask import Flask
from flask.testing import FlaskClient
from app import event_bp, volunteer_bp, notifications_bp, profile_bp, pdf_bp, init_db, login, home
from event_management import find_event
import psycopg2
from unittest.mock import patch, MagicMock
from db import get_db_connection, test_db_connection
import datetime
import app

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(event_bp, url_prefix='/api')
    app.register_blueprint(volunteer_bp, url_prefix='/api')
    app.register_blueprint(notifications_bp, url_prefix='/api')
    app.register_blueprint(profile_bp, url_prefix='/api')
    app.register_blueprint(pdf_bp, url_prefix='/api')
    return app

@pytest.fixture
def client(app: Flask):
    return app.test_client()

def test_create_event_success(client: FlaskClient, mocker):
    mock_conn = mocker.patch('event_management.get_db_connection')
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [1]
    event_data = {
        'eventName': 'Test Event',
        'eventDescription': 'This is a test event',
        'location': 'Test Location',
        'requiredSkills': ['Skill 1', 'Skill 2'],
        'urgency': 'High',
        'eventDate': '2024-12-01'
    }
    response = client.post('/api/events', json=event_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Event created successfully'
    assert 'event_id' in data

def test_create_event_missing_fields(client: FlaskClient):
    event_data = {'eventName': 'Incomplete Event'}
    response = client.post('/api/events', json=event_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Missing required fields in event form'

def test_create_event_invalid_skills(client: FlaskClient):
    event_data = {
        'eventName': 'Test Event',
        'eventDescription': 'This is a test event',
        'location': 'Test Location',
        'requiredSkills': 'Not a list',
        'urgency': 'High',
        'eventDate': '2024-12-01'
    }
    response = client.post('/api/events', json=event_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Required skills must be a list'

def test_create_event_invalid_date(client: FlaskClient):
    event_data = {
        'eventName': 'Test Event',
        'eventDescription': 'This is a test event',
        'location': 'Test Location',
        'requiredSkills': ['Skill 1', 'Skill 2'],
        'urgency': 'High',
        'eventDate': 'invalid-date'
    }
    response = client.post('/api/events', json=event_data)
    assert response.status_code == 400
    data = response.get_json()
    assert data['message'] == 'Invalid date format'

def test_get_events_success(client: FlaskClient, mocker):
    mock_conn = mocker.patch('event_management.get_db_connection')
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [
        (1, 'Event 1', 'Description 1', 'Location 1', ['Skill 1'], 'High', datetime.datetime(2024, 12, 1)),
        (2, 'Event 2', 'Description 2', 'Location 2', ['Skill 2'], 'Low', datetime.datetime(2024, 12, 2)),
    ]
    response = client.get('/api/events')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]['name'] == 'Event 1'

def test_get_events_empty(client: FlaskClient, mocker):
    mock_conn = mocker.patch('event_management.get_db_connection')
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = []
    response = client.get('/api/events')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_events_db_error(client: FlaskClient, mocker):
    mocker.patch('event_management.get_db_connection', side_effect=Exception("Database connection failed"))
    response = client.get('/api/events')
    assert response.status_code == 500
    data = response.get_json()
    assert data['message'] == 'An error occurred while fetching events'

def test_find_event_db_error(mocker):
    mocker.patch('event_management.get_db_connection', side_effect=Exception("Database error"))
    from event_management import find_event
    event = find_event('Test Event')
    assert event is None

def test_get_volunteers(client: FlaskClient, mocker):
    mock_conn = mocker.patch('volunteer_matching.get_db_connection')
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, 'John Doe', ['skill1', 'skill2'])]
    response = client.get('/api/volunteers')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'John Doe'

def test_match_volunteer_success(client: FlaskClient, mocker):
    mock_conn = mocker.patch('volunteer_matching.get_db_connection')
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [1]
    mock_cursor.fetchall.return_value = [(1, 'Event 1')]
    mock_cursor.fetchone.return_value = [1]
    data = {'volunteerName': 'John Doe', 'matchedEvent': 'Event 1'}
    response = client.post('/api/match', json=data)
    assert response.status_code == 201
    response_data = response.get_json()
    assert response_data['message'] == 'Volunteer matched successfully'

def test_match_volunteer_missing_fields(client: FlaskClient):
    data = {'volunteerName': 'John Doe'}
    response = client.post('/api/match', json=data)
    assert response.status_code == 400
    response_data = response.get_json()
    assert response_data['message'] == 'Missing required fields'

def test_get_matches(client: FlaskClient, mocker):
    mock_conn = mocker.patch('volunteer_matching.get_db_connection')
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, 'John Doe', 'Event 1', datetime.datetime(2024, 12, 1))]
    response = client.get('/api/match')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['volunteer_name'] == 'John Doe'

def test_event_history(client: FlaskClient, mocker):
    mock_conn = mocker.patch('volunteer_matching.get_db_connection')
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = [(1, 'Event 1', 'Description 1', 'Location 1', datetime.datetime(2024, 12, 1))]
    data = {'user_id': 1}
    response = client.get('/api/eventhistory', query_string=data)
    assert response.status_code == 200
    event_data = response.get_json()
    assert len(event_data) == 1
    assert event_data[0]['name'] == 'Event 1'

def test_create_volunteer_profile_success(client: FlaskClient, mocker):
    mock_conn = mocker.patch('ProfileForm.get_db_connection')
    mock_cursor = mock_conn.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = [1]
    data = {
        'fullName': 'John Doe',
        'address1': '123 Main St',
        'address2': 'Apt 4B',
        'city': 'Cityville',
        'state': 'ST',
        'zipCode': '12345',
        'preferences': ['community work'],
        'availability': ['2024-11-01', '2024-11-02'],
        'skills': ['problem-solving']
    }
    response = client.post('/api/profile', json=data)
    assert response.status_code == 201
    assert response.json['message'] == 'Volunteer profile successfully created'
    assert response.json['volunteer_id'] == 1

def test_create_volunteer_profile_missing_fields(client: FlaskClient):
    data = {
        'address1': '123 Main St',
        'city': 'Cityville',
        'state': 'ST',
        'zipCode': '12345',
        'skills': ['problem-solving']
    }
    response = client.post('/api/profile', json=data)
    assert response.status_code == 400
    assert response.json['error'] == 'Missing required fields in profile'

def test_create_volunteer_profile_db_error(client: FlaskClient, mocker):
    mock_conn = mocker.patch('ProfileForm.get_db_connection')
    mock_conn.return_value.cursor.side_effect = Exception("Database error")
    data = {
        'fullName': 'John Doe',
        'address1': '123 Main St',
        'address2': 'Apt 4B',
        'city': 'Cityville',
        'state': 'ST',
        'zipCode': '12345',
        'preferences': ['community work'],
        'availability': ['2024-11-01', '2024-11-02'],
        'skills': ['problem-solving']
    }
    response = client.post('/api/profile', json=data)
    assert response.status_code == 500
    assert response.json['message'] == 'An error occurred while creating volunteer profile'


def test_create_volunteer_profile_missing_skills(client: FlaskClient):
    data = {
        'fullName': 'Jane Doe',
        'address1': '456 Elm St',
        'address2': 'Apt 5C',
        'city': 'Townsville',
        'state': 'TX',
        'zipCode': '54321',
        'preferences': ['education'],
        'availability': ['2024-12-01'],
        'skills': None
    }
    response = client.post('/api/profile', json=data)
    assert response.status_code == 400
    assert response.json['error'] == 'Missing required fields in profile'

@patch('psycopg2.connect')
def test_get_db_connection_success(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    conn = get_db_connection()
    mock_connect.assert_called_with(
        host="localhost",
        database="volunteer_management_db",
        user="postgres",
        password="password",
        port="5432"
    )
    assert conn == mock_conn

@patch('psycopg2.connect')
def test_test_db_connection_failure(mock_connect):
    mock_connect.side_effect = psycopg2.OperationalError("Database connection failed")
    with patch('builtins.print') as mock_print:
        test_db_connection()
        mock_print.assert_any_call("ERROR while connecting to db: Database connection failed")

@patch('psycopg2.connect')
def test_test_db_connection_success(mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    with patch('builtins.print') as mock_print:
        test_db_connection()
        mock_print.assert_any_call("Connection to db successful")

@patch('psycopg2.connect')
def test_test_db_connection_failure(mock_connect):
    mock_connect.side_effect = psycopg2.OperationalError("Database connection failed")
    with patch('builtins.print') as mock_print:
        test_db_connection()
        mock_print.assert_any_call("ERROR while connecting to db: {'message': 'Database connection failed'}")

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == "Backend server is running"

@patch('db.get_db_connection')
def test_init_db(mock_get_db_connection):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    init_db()
    mock_cursor.execute.assert_any_call('''CREATE TABLE IF NOT EXISTS usercredentials (id varchar(100) PRIMARY KEY, password varchar(60));''')
    mock_cursor.execute.assert_any_call('''CREATE TABLE IF NOT EXISTS volunteers(id SERIAL PRIMARY KEY, name VARCHAR(120), address1 VARCHAR(100), address2 VARCHAR(100), city VARCHAR(100), state VARCHAR(2) REFERENCES states(code), zip_code VARCHAR(9), preferences TEXT, availability DATE[], skills TEXT[]);''')
    mock_cursor.execute.assert_any_call('''CREATE TABLE IF NOT EXISTS volunteer_history(id SERIAL PRIMARY KEY, volunteer_id INTEGER NOT NULL, event_id INTEGER NOT NULL, participation_date DATE DEFAULT CURRENT_DATE, FOREIGN KEY (volunteer_id) REFERENCES volunteers(id), FOREIGN KEY (event_id) REFERENCES events(id));''')
    mock_cursor.execute.assert_any_call('''CREATE TABLE IF NOT EXISTS events(id SERIAL PRIMARY KEY, name VARCHAR(120), description TEXT, location VARCHAR(120), required_skills TEXT[], urgency VARCHAR(50), date DATE); ''')
    mock_conn.commit.assert_called_once()

@patch('db.get_db_connection')
def test_login_success(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ['password']
    response = client.post('/login', data={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 200
    assert response.json == {'login': 1}

@patch('db.get_db_connection')
def test_login_failure(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ['wrongpassword']
    response = client.post('/login', data={'username': 'testuser', 'password': 'password'})
    assert response.status_code == 200
    assert response.json == {'login': 0}

@patch('db.get_db_connection')
def test_login_missing_credentials(mock_get_db_connection, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    response = client.post('/login', data={})
    assert response.status_code == 400
    assert response.json == {'login': 0}
