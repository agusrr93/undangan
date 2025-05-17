-- Enable UUID extension if not already
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop table if exists
DROP TABLE IF EXISTS comment;

-- Create table
CREATE TABLE comment (
    uuid UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    presence BOOLEAN DEFAULT TRUE,
    comment TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    gif_url VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    love INTEGER DEFAULT 0,
    owner_uuid UUID,
    comments JSON DEFAULT '[]'::json
);