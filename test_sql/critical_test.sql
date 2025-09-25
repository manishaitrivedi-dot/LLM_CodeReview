-- critical_test.sql

-- Table to store user login info (BAD PRACTICE: storing plain text passwords)
CREATE TABLE users (
    --test for inline comment 1
    user_id INT PRIMARY KEY,
    --test for inline comment 2 
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100),   -- ❌ Critical: Plaintext password storage
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert dummy users
INSERT INTO users (user_id, username, password)
VALUES
    (1, 'admin', 'admin123'),   -- ❌ Critical: Weak hardcoded password
    (2, 'test', 'password'),
    (1, 'test11', 'password@3133');

-- Vulnerable query (SQL injection risk: directly concatenating user input)
-- ❌ Critical: This should use parameterized queries instead
SET @input_username = 'admin''; DROP TABLE users; --';
SET @query = 'SELECT * FROM users WHERE username = ''' || @input_username || '''';
EXECUTE IMMEDIATE @query;

-- Another risky query (DELETE without WHERE clause)
DELETE FROM users;
