-- sql_dynamic_mysql.sql
-- CRITICAL: dynamic SQL built by concatenation and EXECUTED
 
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100)
);

DELIMITER $$

CREATE PROCEDURE get_user_info(IN username VARCHAR(100))
BEGIN
  SET @q = CONCAT('SELECT * FROM users WHERE name = \'', username, '\'');
  PREPARE stmt FROM @q;      -- unsafe: prepared from concatenated user input
  EXECUTE stmt;
  DEALLOCATE PREPARE stmt;
END$$

DELIMITER ;
