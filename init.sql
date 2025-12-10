-- -------------------------------------------------------
-- init.sql
-- This script initializes the required schema for RDS
-- and local Postgres (docker-compose).
-- -------------------------------------------------------

-- Ensure the 'users' table exists.
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE
);
