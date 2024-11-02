DROP TABLE IF EXISTS events;
CREATE TABLE events(id SERIAL PRIMARY KEY, name VARCHAR(120), description TEXT, location VARCHAR(120), required_skills TEXT[], urgency VARCHAR(50), date DATE);