CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL DEFAULT 'admin123', -- ❌ Critical security issue
    email VARCHAR(100)
);

-- Inserting sample user
INSERT INTO users (user_id, username, password, email)
VALUES (1, 'test_user', 'password123', 'test@example.com'); 
