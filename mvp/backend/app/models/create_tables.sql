-- SQL script to create tables for users and activity_log

-- Create the users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    isadmin BOOLEAN DEFAULT FALSE
);

-- Create the activity_log table
CREATE TABLE activity_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    activity_type VARCHAR(255) NOT NULL,  -- e.g., 'login', 'image ocr'
    description TEXT,                     -- Additional info about the activity
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
