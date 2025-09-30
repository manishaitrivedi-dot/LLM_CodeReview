-- Generated bad SQL file for testing. Timestamp: 20250925_125532
-- Contains intentional security, correctness, and performance issues.


-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_2 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_2 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5079'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_3 a
JOIN huge_table_3_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_4
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_5 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_6 a
JOIN huge_table_6_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_8 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_8 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4037'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_9 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_9 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4072'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 10
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_11 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_11 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3375'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_13 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_13 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4445'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_18 a
JOIN huge_table_18_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_19 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_19 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6959'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_20
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 20
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_21
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_23 a
JOIN huge_table_23_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_25 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_25 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4683'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_26 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_30
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 30
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_32
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_33
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_34 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_35 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_35 (user_id, username, password, email)
VALUES (35, 'user_35', 'P@ss_1040', 'user_35@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_37 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_37 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1130'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_39
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_40 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_40 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2172'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 40
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_41 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_42 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_45
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_46 a
JOIN huge_table_46_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_47 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_48 a
JOIN huge_table_48_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_49 a
JOIN huge_table_49_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_50 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_50 (user_id, username, password, email)
VALUES (50, 'user_50', 'P@ss_7001', 'user_50@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 50
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_54 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_55 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_55 (user_id, username, password, email)
VALUES (55, 'user_55', 'P@ss_2331', 'user_55@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_57
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 60
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_61
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_62
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_64 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_65
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_66 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_66 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2955'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_68 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_69 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_69 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9617'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 70
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_72 a
JOIN huge_table_72_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_73 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_73 (user_id, username, password, email)
VALUES (73, 'user_73', 'P@ss_7481', 'user_73@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_74
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_76
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_78 a
JOIN huge_table_78_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_79 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_79 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6042'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 80
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_81 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_81 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8094'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_84 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_84 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7857'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_85 a
JOIN huge_table_85_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_89 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_89 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6662'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 90
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_93 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_93 (user_id, username, password, email)
VALUES (93, 'user_93', 'P@ss_2276', 'user_93@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_95 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_95 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9179'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_96 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_96 (user_id, username, password, email)
VALUES (96, 'user_96', 'P@ss_2527', 'user_96@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_97 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_97 (user_id, username, password, email)
VALUES (97, 'user_97', 'P@ss_7304', 'user_97@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_98 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_98 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2059'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_99 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 100
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_101 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_101 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5666'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_104
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_105 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_105 (user_id, username, password, email)
VALUES (105, 'user_105', 'P@ss_4652', 'user_105@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_106 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_106 (user_id, username, password, email)
VALUES (106, 'user_106', 'P@ss_8131', 'user_106@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_107
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_109
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 110
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_111 a
JOIN huge_table_111_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_113 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_113 (user_id, username, password, email)
VALUES (113, 'user_113', 'P@ss_4211', 'user_113@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_115
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_116 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_116 (user_id, username, password, email)
VALUES (116, 'user_116', 'P@ss_6783', 'user_116@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_117 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_119
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_120 a
JOIN huge_table_120_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 120
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_121 a
JOIN huge_table_121_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_122 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_124 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_124 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6838'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_125 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_125 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1234'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_128 a
JOIN huge_table_128_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_129 a
JOIN huge_table_129_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_130 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 130
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_134
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_135 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_135 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3873'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_136
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_137 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_137 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2585'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_140
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 140
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_141 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_143 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_145 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_145 (user_id, username, password, email)
VALUES (145, 'user_145', 'P@ss_5106', 'user_145@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_147 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_148
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_150 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_150 (user_id, username, password, email)
VALUES (150, 'user_150', 'P@ss_9787', 'user_150@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 150
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_151 a
JOIN huge_table_151_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_152 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_152 (user_id, username, password, email)
VALUES (152, 'user_152', 'P@ss_2696', 'user_152@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_153 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_153 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3120'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_154 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_157 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_157 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8378'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_158
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_159
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 160
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_163 a
JOIN huge_table_163_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_164 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_170 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_170 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9147'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 170
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_173 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_174 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_174 (user_id, username, password, email)
VALUES (174, 'user_174', 'P@ss_6167', 'user_174@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_175 a
JOIN huge_table_175_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_176 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_176 (user_id, username, password, email)
VALUES (176, 'user_176', 'P@ss_5779', 'user_176@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_177 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_177 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7961'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_180 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_180 (user_id, username, password, email)
VALUES (180, 'user_180', 'P@ss_5874', 'user_180@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 180
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_183 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_183 (user_id, username, password, email)
VALUES (183, 'user_183', 'P@ss_6987', 'user_183@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_186 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_186 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8714'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_187 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_187 (user_id, username, password, email)
VALUES (187, 'user_187', 'P@ss_5772', 'user_187@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_188 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_188 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8527'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_189 a
JOIN huge_table_189_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 190
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_191 a
JOIN huge_table_191_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_196 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_196 (user_id, username, password, email)
VALUES (196, 'user_196', 'P@ss_7084', 'user_196@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_198 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_198 (user_id, username, password, email)
VALUES (198, 'user_198', 'P@ss_7284', 'user_198@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_200 a
JOIN huge_table_200_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 200
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_201 a
JOIN huge_table_201_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_204 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_204 (user_id, username, password, email)
VALUES (204, 'user_204', 'P@ss_5867', 'user_204@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_205 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_205 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2787'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_207 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_209 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_209 (user_id, username, password, email)
VALUES (209, 'user_209', 'P@ss_3771', 'user_209@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 210
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_211
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_213 a
JOIN huge_table_213_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_215 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_215 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6465'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_216 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_216 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9725'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_218 a
JOIN huge_table_218_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_219
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_220
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 220
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_221 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_221 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2156'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_223 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_223 (user_id, username, password, email)
VALUES (223, 'user_223', 'P@ss_5610', 'user_223@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_224
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_225 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_226 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_227 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_227 (user_id, username, password, email)
VALUES (227, 'user_227', 'P@ss_9745', 'user_227@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_228
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_229 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_229 (user_id, username, password, email)
VALUES (229, 'user_229', 'P@ss_3143', 'user_229@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 230
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_231 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_231 (user_id, username, password, email)
VALUES (231, 'user_231', 'P@ss_5038', 'user_231@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_232 a
JOIN huge_table_232_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_233 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_236 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_236 (user_id, username, password, email)
VALUES (236, 'user_236', 'P@ss_4525', 'user_236@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_237 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_237 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7723'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_239 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_239 (user_id, username, password, email)
VALUES (239, 'user_239', 'P@ss_3984', 'user_239@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_240 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 240
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_241 a
JOIN huge_table_241_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_242 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_242 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4150'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_244 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_244 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5683'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_245 a
JOIN huge_table_245_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_246
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_247 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_247 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4019'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_248 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_249 a
JOIN huge_table_249_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_250 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 250
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_251 a
JOIN huge_table_251_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_252 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_252 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5625'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_254 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_254 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6586'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_256
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_257 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_257 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2173'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_259 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_259 (user_id, username, password, email)
VALUES (259, 'user_259', 'P@ss_4252', 'user_259@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 260
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_262 a
JOIN huge_table_262_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_264 a
JOIN huge_table_264_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_270 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_270 (user_id, username, password, email)
VALUES (270, 'user_270', 'P@ss_2209', 'user_270@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 270
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_271 a
JOIN huge_table_271_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_272 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_273 a
JOIN huge_table_273_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_275 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_276
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 280
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_281 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_282 a
JOIN huge_table_282_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_283
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_286 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_286 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9915'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_287 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_287 (user_id, username, password, email)
VALUES (287, 'user_287', 'P@ss_3875', 'user_287@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_289 a
JOIN huge_table_289_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_290 a
JOIN huge_table_290_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 290
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_291 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_291 (user_id, username, password, email)
VALUES (291, 'user_291', 'P@ss_1363', 'user_291@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_293
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_295 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_295 (user_id, username, password, email)
VALUES (295, 'user_295', 'P@ss_6230', 'user_295@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_296 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_296 (user_id, username, password, email)
VALUES (296, 'user_296', 'P@ss_3737', 'user_296@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_298
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 300
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_301 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_303 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_305 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_305 (user_id, username, password, email)
VALUES (305, 'user_305', 'P@ss_2530', 'user_305@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_307 a
JOIN huge_table_307_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_308 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_308 (user_id, username, password, email)
VALUES (308, 'user_308', 'P@ss_5958', 'user_308@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_309 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_310
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 310
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_311 a
JOIN huge_table_311_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_315 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_319 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_319 (user_id, username, password, email)
VALUES (319, 'user_319', 'P@ss_6632', 'user_319@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_320 a
JOIN huge_table_320_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 320
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_322 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_322 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5342'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_323 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_323 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5899'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_325 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_326
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_327 a
JOIN huge_table_327_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_330 a
JOIN huge_table_330_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 330
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_333
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_335
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_336 a
JOIN huge_table_336_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_340 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_340 (user_id, username, password, email)
VALUES (340, 'user_340', 'P@ss_6598', 'user_340@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 340
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_343
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_344 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_344 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1382'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_346 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_346 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3541'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_347 a
JOIN huge_table_347_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_348 a
JOIN huge_table_348_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_349
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 350
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_353
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_355 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_355 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7751'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_357 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_357 (user_id, username, password, email)
VALUES (357, 'user_357', 'P@ss_4191', 'user_357@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_358 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_358 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6026'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_359
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_360
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 360
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_361 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_361 (user_id, username, password, email)
VALUES (361, 'user_361', 'P@ss_2373', 'user_361@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_362 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_364
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_366 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_366 (user_id, username, password, email)
VALUES (366, 'user_366', 'P@ss_1294', 'user_366@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_369 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_369 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1956'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 370
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_372 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_372 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5803'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_373
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_374 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_375 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_375 (user_id, username, password, email)
VALUES (375, 'user_375', 'P@ss_4984', 'user_375@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_376 a
JOIN huge_table_376_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_377 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_377 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1598'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_380 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_380 (user_id, username, password, email)
VALUES (380, 'user_380', 'P@ss_9985', 'user_380@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 380
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_383 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_384 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_384 (user_id, username, password, email)
VALUES (384, 'user_384', 'P@ss_4368', 'user_384@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_385
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_386 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_386 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6269'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_387
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_388 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_389 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_389 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2179'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_390 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 390
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_392 a
JOIN huge_table_392_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_395 a
JOIN huge_table_395_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_396 a
JOIN huge_table_396_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_398 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_398 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1128'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_399
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_400 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_400 (user_id, username, password, email)
VALUES (400, 'user_400', 'P@ss_1928', 'user_400@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 400
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_401 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_402 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_402 (user_id, username, password, email)
VALUES (402, 'user_402', 'P@ss_3584', 'user_402@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_403 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_404 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_404 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7244'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_407
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_408 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_409 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_410 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 410
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_414 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_415
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_416 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_417 a
JOIN huge_table_417_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_418
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_419 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 420
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_424
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_426 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_426 (user_id, username, password, email)
VALUES (426, 'user_426', 'P@ss_8983', 'user_426@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_428 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_430
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 430
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_431
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_433 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_433 (user_id, username, password, email)
VALUES (433, 'user_433', 'P@ss_6397', 'user_433@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_434 a
JOIN huge_table_434_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_437 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_437 (user_id, username, password, email)
VALUES (437, 'user_437', 'P@ss_4932', 'user_437@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_438 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_438 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3667'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_439 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_439 (user_id, username, password, email)
VALUES (439, 'user_439', 'P@ss_5803', 'user_439@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 440
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_441 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_442 a
JOIN huge_table_442_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_444 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_446 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_446 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2178'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_447 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_447 (user_id, username, password, email)
VALUES (447, 'user_447', 'P@ss_5795', 'user_447@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_448
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_450
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 450
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_451
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_452
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_455 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_456 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_456 (user_id, username, password, email)
VALUES (456, 'user_456', 'P@ss_5445', 'user_456@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_457 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_460 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_460 (user_id, username, password, email)
VALUES (460, 'user_460', 'P@ss_2045', 'user_460@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 460
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_462 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_462 (user_id, username, password, email)
VALUES (462, 'user_462', 'P@ss_9311', 'user_462@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_464 a
JOIN huge_table_464_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_465 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_465 (user_id, username, password, email)
VALUES (465, 'user_465', 'P@ss_1299', 'user_465@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_468
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_470 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_470 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4346'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 470
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_472 a
JOIN huge_table_472_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_474 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_474 (user_id, username, password, email)
VALUES (474, 'user_474', 'P@ss_6442', 'user_474@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_479 a
JOIN huge_table_479_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_480 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 480
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_483 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_484 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_484 (user_id, username, password, email)
VALUES (484, 'user_484', 'P@ss_7921', 'user_484@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_485
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_486 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_489
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_490 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 490
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_491 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_491 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7113'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_492 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_493 a
JOIN huge_table_493_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_494 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_495 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_495 (user_id, username, password, email)
VALUES (495, 'user_495', 'P@ss_6791', 'user_495@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_496 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_496 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9508'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_497 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_498
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_499 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 500
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_501 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_501 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4393'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_503 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_503 (user_id, username, password, email)
VALUES (503, 'user_503', 'P@ss_5382', 'user_503@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_504
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_507 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_507 (user_id, username, password, email)
VALUES (507, 'user_507', 'P@ss_4402', 'user_507@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_508 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 510
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_511 a
JOIN huge_table_511_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_512 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_512 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6726'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_513 a
JOIN huge_table_513_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_517 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_517 (user_id, username, password, email)
VALUES (517, 'user_517', 'P@ss_2839', 'user_517@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_519 a
JOIN huge_table_519_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_520 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_520 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4294'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 520
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_521 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_521 (user_id, username, password, email)
VALUES (521, 'user_521', 'P@ss_5014', 'user_521@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_523 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_524 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_524 (user_id, username, password, email)
VALUES (524, 'user_524', 'P@ss_8441', 'user_524@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_527 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_528
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_529
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_530 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 530
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_531 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_531 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5321'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_532 a
JOIN huge_table_532_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_533 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_533 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8110'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_534 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_534 (user_id, username, password, email)
VALUES (534, 'user_534', 'P@ss_5214', 'user_534@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_535 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_535 (user_id, username, password, email)
VALUES (535, 'user_535', 'P@ss_1619', 'user_535@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_536 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_536 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1872'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_537
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_538 a
JOIN huge_table_538_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 540
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_542 a
JOIN huge_table_542_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_544 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_544 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8849'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_546 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_547 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_549 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_549 (user_id, username, password, email)
VALUES (549, 'user_549', 'P@ss_5858', 'user_549@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 550
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_551 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_551 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8949'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_552 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_553 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_555 a
JOIN huge_table_555_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_556 a
JOIN huge_table_556_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_557
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_558
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_560
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 560
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_561 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_561 (user_id, username, password, email)
VALUES (561, 'user_561', 'P@ss_8305', 'user_561@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_562 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_563 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_564 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_564 (user_id, username, password, email)
VALUES (564, 'user_564', 'P@ss_4398', 'user_564@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_565 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_568 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_568 (user_id, username, password, email)
VALUES (568, 'user_568', 'P@ss_9223', 'user_568@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_569 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_569 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3309'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_570
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 570
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_572 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_573 a
JOIN huge_table_573_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_574 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_574 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2642'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_575 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_575 (user_id, username, password, email)
VALUES (575, 'user_575', 'P@ss_7491', 'user_575@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_576
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_577 a
JOIN huge_table_577_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_579 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 580
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_582 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_582 (user_id, username, password, email)
VALUES (582, 'user_582', 'P@ss_1756', 'user_582@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_584 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_586 a
JOIN huge_table_586_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_587 a
JOIN huge_table_587_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_588 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_588 (user_id, username, password, email)
VALUES (588, 'user_588', 'P@ss_4942', 'user_588@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_589 a
JOIN huge_table_589_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_590 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 590
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_591 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_591 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4600'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_592 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_592 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1016'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_594 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_594 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4135'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_595 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_595 (user_id, username, password, email)
VALUES (595, 'user_595', 'P@ss_8107', 'user_595@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_597 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_597 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6315'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_598
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_599 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 600
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_601 a
JOIN huge_table_601_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_602 a
JOIN huge_table_602_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_604 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_604 (user_id, username, password, email)
VALUES (604, 'user_604', 'P@ss_6919', 'user_604@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_605 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_605 (user_id, username, password, email)
VALUES (605, 'user_605', 'P@ss_1392', 'user_605@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_607 a
JOIN huge_table_607_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_608
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_609
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 610
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_613 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_613 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3978'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_615 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_615 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3325'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_618 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_618 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3103'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_619 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_619 (user_id, username, password, email)
VALUES (619, 'user_619', 'P@ss_2935', 'user_619@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 620
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_621 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_621 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7759'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_622 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_622 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3474'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_624
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_629 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_629 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6200'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 630
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_631 a
JOIN huge_table_631_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_632 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_632 (user_id, username, password, email)
VALUES (632, 'user_632', 'P@ss_6449', 'user_632@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_633 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_634
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_635 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_635 (user_id, username, password, email)
VALUES (635, 'user_635', 'P@ss_1532', 'user_635@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_637 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_640 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_640 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1166'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 640
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_641
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_642
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_644 a
JOIN huge_table_644_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_645
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_646
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_647 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_647 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9473'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_649 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_649 (user_id, username, password, email)
VALUES (649, 'user_649', 'P@ss_7830', 'user_649@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 650
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_651 a
JOIN huge_table_651_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_652 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_652 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3586'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_654 a
JOIN huge_table_654_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_657 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_658 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_659 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_659 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8980'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 660
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_662 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_663 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_668 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_668 (user_id, username, password, email)
VALUES (668, 'user_668', 'P@ss_8631', 'user_668@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_669
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_670 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_670 (user_id, username, password, email)
VALUES (670, 'user_670', 'P@ss_1938', 'user_670@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 670
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_672
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_675 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_675 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2371'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_677
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_678 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_678 (user_id, username, password, email)
VALUES (678, 'user_678', 'P@ss_6074', 'user_678@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_679 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_679 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8792'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 680
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_681 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_682 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_682 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5483'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_684
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_685 a
JOIN huge_table_685_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_689
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 690
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_691 a
JOIN huge_table_691_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_692 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_692 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7833'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_693 a
JOIN huge_table_693_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_694 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_694 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7097'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_695 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_695 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2895'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_696 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_696 (user_id, username, password, email)
VALUES (696, 'user_696', 'P@ss_1502', 'user_696@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_697
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_699
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_700 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 700
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_701 a
JOIN huge_table_701_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_703 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_703 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5965'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_704 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_706 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_707 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_707 (user_id, username, password, email)
VALUES (707, 'user_707', 'P@ss_6669', 'user_707@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_710
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 710
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_711 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_711 (user_id, username, password, email)
VALUES (711, 'user_711', 'P@ss_2956', 'user_711@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_712 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_712 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1131'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_713 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_713 (user_id, username, password, email)
VALUES (713, 'user_713', 'P@ss_9972', 'user_713@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_714 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_714 (user_id, username, password, email)
VALUES (714, 'user_714', 'P@ss_1305', 'user_714@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_715 a
JOIN huge_table_715_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_717 a
JOIN huge_table_717_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_720 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 720
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_721 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_721 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2586'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_722 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_722 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3103'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_725 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_725 (user_id, username, password, email)
VALUES (725, 'user_725', 'P@ss_5647', 'user_725@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_726
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_727 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_729
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_730 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 730
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_731 a
JOIN huge_table_731_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_733
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_735
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_736
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_737 a
JOIN huge_table_737_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_738 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_738 (user_id, username, password, email)
VALUES (738, 'user_738', 'P@ss_5187', 'user_738@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_739
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 740
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_741 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_741 (user_id, username, password, email)
VALUES (741, 'user_741', 'P@ss_1685', 'user_741@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_743 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_744 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_744 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4045'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_745 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_745 (user_id, username, password, email)
VALUES (745, 'user_745', 'P@ss_4115', 'user_745@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_746 a
JOIN huge_table_746_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_747
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_748
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_749 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_749 (user_id, username, password, email)
VALUES (749, 'user_749', 'P@ss_7253', 'user_749@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_750 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_750 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5782'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 750
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_751 a
JOIN huge_table_751_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_755 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_756 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_756 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2549'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_757 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 760
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_761
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_762 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_762 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3444'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_765 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_765 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2202'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_766 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_766 (user_id, username, password, email)
VALUES (766, 'user_766', 'P@ss_4465', 'user_766@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 770
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_773 a
JOIN huge_table_773_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_774 a
JOIN huge_table_774_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_775
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_776 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_776 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1308'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_778
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 780
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_781 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_782 a
JOIN huge_table_782_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_784 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_785 a
JOIN huge_table_785_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_787 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_787 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3930'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 790
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_792
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_793 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_794 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_794 (user_id, username, password, email)
VALUES (794, 'user_794', 'P@ss_8417', 'user_794@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_795 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_795 (user_id, username, password, email)
VALUES (795, 'user_795', 'P@ss_8119', 'user_795@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_796
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_800 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_800 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1598'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 800
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_801
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_802 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_804 a
JOIN huge_table_804_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_806
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_807 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_808 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_808 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7242'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_809 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_809 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6708'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_810 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_810 (user_id, username, password, email)
VALUES (810, 'user_810', 'P@ss_8176', 'user_810@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 810
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_811 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_811 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7171'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_812 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_813
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_814 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_814 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1218'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_815 a
JOIN huge_table_815_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_817 a
JOIN huge_table_817_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_818 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 820
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_821 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_821 (user_id, username, password, email)
VALUES (821, 'user_821', 'P@ss_2754', 'user_821@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_822 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_822 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1182'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_823
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_824 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_824 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5287'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_826
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_829 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_829 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9511'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_830
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 830
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_832 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_832 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5317'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_833 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_835 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_835 (user_id, username, password, email)
VALUES (835, 'user_835', 'P@ss_6497', 'user_835@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_838 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_838 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7651'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_840 a
JOIN huge_table_840_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 840
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_842
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_843 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_843 (user_id, username, password, email)
VALUES (843, 'user_843', 'P@ss_1338', 'user_843@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_844 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_844 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2976'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_846 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_846 (user_id, username, password, email)
VALUES (846, 'user_846', 'P@ss_2360', 'user_846@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_848 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_849 a
JOIN huge_table_849_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_850 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_850 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8727'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 850
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_851 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_851 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9947'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_852 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_852 (user_id, username, password, email)
VALUES (852, 'user_852', 'P@ss_2396', 'user_852@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_853 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_853 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9648'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_855 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_855 (user_id, username, password, email)
VALUES (855, 'user_855', 'P@ss_3300', 'user_855@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_856 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_856 (user_id, username, password, email)
VALUES (856, 'user_856', 'P@ss_8449', 'user_856@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_858
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_860
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 860
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_861 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_861 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3662'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_862 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_862 (user_id, username, password, email)
VALUES (862, 'user_862', 'P@ss_5838', 'user_862@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_865 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_866
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_868
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_869 a
JOIN huge_table_869_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 870
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_872 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_872 (user_id, username, password, email)
VALUES (872, 'user_872', 'P@ss_7089', 'user_872@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_873
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_874 a
JOIN huge_table_874_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_875 a
JOIN huge_table_875_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_876 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_877
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_879 a
JOIN huge_table_879_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_880 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_880 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5013'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 880
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_881
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_882 a
JOIN huge_table_882_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_885 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_886 a
JOIN huge_table_886_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_887 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_888 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_888 (user_id, username, password, email)
VALUES (888, 'user_888', 'P@ss_3237', 'user_888@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_889
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_890
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 890
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_891 a
JOIN huge_table_891_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_892 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_894 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_894 (user_id, username, password, email)
VALUES (894, 'user_894', 'P@ss_7102', 'user_894@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_896 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_896 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9279'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_898 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_898 (user_id, username, password, email)
VALUES (898, 'user_898', 'P@ss_3076', 'user_898@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_899 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_900 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 900
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_901 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_901 (user_id, username, password, email)
VALUES (901, 'user_901', 'P@ss_6388', 'user_901@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_902 a
JOIN huge_table_902_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_904 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_904 (user_id, username, password, email)
VALUES (904, 'user_904', 'P@ss_4690', 'user_904@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_907 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_908
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_909 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 910
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_912 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_912 (user_id, username, password, email)
VALUES (912, 'user_912', 'P@ss_2494', 'user_912@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_916 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_916 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6890'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_917 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_917 (user_id, username, password, email)
VALUES (917, 'user_917', 'P@ss_6697', 'user_917@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_918 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_918 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3614'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_919 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_919 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7943'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 920
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_921 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_921 (user_id, username, password, email)
VALUES (921, 'user_921', 'P@ss_9043', 'user_921@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_923
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_924
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_927 a
JOIN huge_table_927_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_929 a
JOIN huge_table_929_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_930 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_930 (user_id, username, password, email)
VALUES (930, 'user_930', 'P@ss_4133', 'user_930@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 930
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_931
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_932 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_936
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_937
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_938 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_939
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_940
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 940
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_941 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_941 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1517'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_945 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_945 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9370'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_946 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_947 a
JOIN huge_table_947_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_948 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_948 (user_id, username, password, email)
VALUES (948, 'user_948', 'P@ss_3576', 'user_948@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_949 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_950 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_950 (user_id, username, password, email)
VALUES (950, 'user_950', 'P@ss_9163', 'user_950@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 950
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_953 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_953 (user_id, username, password, email)
VALUES (953, 'user_953', 'P@ss_2566', 'user_953@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_954 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_954 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8617'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_958 a
JOIN huge_table_958_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_959 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_960 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_960 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9887'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 960
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_963 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_963 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5227'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_964 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_964 (user_id, username, password, email)
VALUES (964, 'user_964', 'P@ss_2842', 'user_964@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_965 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_965 (user_id, username, password, email)
VALUES (965, 'user_965', 'P@ss_9708', 'user_965@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_966 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_966 (user_id, username, password, email)
VALUES (966, 'user_966', 'P@ss_3543', 'user_966@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_967 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_967 (user_id, username, password, email)
VALUES (967, 'user_967', 'P@ss_7229', 'user_967@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_970 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 970
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_973 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_975
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_976 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_976 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7598'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_977 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_979
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 980
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_981 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_981 (user_id, username, password, email)
VALUES (981, 'user_981', 'P@ss_3779', 'user_981@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_984 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_984 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2316'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_985 a
JOIN huge_table_985_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_987 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_987 (user_id, username, password, email)
VALUES (987, 'user_987', 'P@ss_9380', 'user_987@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_988 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_988 (user_id, username, password, email)
VALUES (988, 'user_988', 'P@ss_7862', 'user_988@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_990 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_990 (user_id, username, password, email)
VALUES (990, 'user_990', 'P@ss_1919', 'user_990@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 990
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_993 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_993 (user_id, username, password, email)
VALUES (993, 'user_993', 'P@ss_3755', 'user_993@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_995 a
JOIN huge_table_995_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_996
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_998
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_999
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1000 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1000 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8291'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1000
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1003 a
JOIN huge_table_1003_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1008 a
JOIN huge_table_1008_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1009 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1009 (user_id, username, password, email)
VALUES (1009, 'user_1009', 'P@ss_1019', 'user_1009@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1010 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1010
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1011 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1011 (user_id, username, password, email)
VALUES (1011, 'user_1011', 'P@ss_1572', 'user_1011@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1012 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1012 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5052'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1014 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1014 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7259'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1015 a
JOIN huge_table_1015_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1017 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1017 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1567'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1018 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1018 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9968'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1020
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1022 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1023 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1023 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9779'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1024 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1024 (user_id, username, password, email)
VALUES (1024, 'user_1024', 'P@ss_9841', 'user_1024@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1029
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1030 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1030
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1031 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1032 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1032 (user_id, username, password, email)
VALUES (1032, 'user_1032', 'P@ss_1270', 'user_1032@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1033 a
JOIN huge_table_1033_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1034 a
JOIN huge_table_1034_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1037 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1037 (user_id, username, password, email)
VALUES (1037, 'user_1037', 'P@ss_3979', 'user_1037@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1038 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1039 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1039 (user_id, username, password, email)
VALUES (1039, 'user_1039', 'P@ss_4049', 'user_1039@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1040 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1040 (user_id, username, password, email)
VALUES (1040, 'user_1040', 'P@ss_1330', 'user_1040@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1040
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1042 a
JOIN huge_table_1042_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1045
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1046 a
JOIN huge_table_1046_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1047
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1049 a
JOIN huge_table_1049_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1050 a
JOIN huge_table_1050_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1050
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1051 a
JOIN huge_table_1051_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1053 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1053 (user_id, username, password, email)
VALUES (1053, 'user_1053', 'P@ss_6088', 'user_1053@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1056 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1056 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9076'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1057 a
JOIN huge_table_1057_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1059 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1059 (user_id, username, password, email)
VALUES (1059, 'user_1059', 'P@ss_2110', 'user_1059@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1060 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1060 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7724'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1060
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1061 a
JOIN huge_table_1061_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1062 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1062 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6085'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1063 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1064 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1065 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1066
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1068 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1069 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1069 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9636'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1070 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1070 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1423'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1070
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1071 a
JOIN huge_table_1071_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1073 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1078 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1078 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3502'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1079 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1079 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9441'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1080
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1081 a
JOIN huge_table_1081_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1082 a
JOIN huge_table_1082_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1085 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1086 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1086 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9612'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1087 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1090 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1090 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7900'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1090
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1091 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1091 (user_id, username, password, email)
VALUES (1091, 'user_1091', 'P@ss_2877', 'user_1091@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1093
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1095
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1096 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1096 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2937'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1099 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1099 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6780'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1100 a
JOIN huge_table_1100_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1100
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1101
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1102 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1103
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1104 a
JOIN huge_table_1104_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1105 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1107 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1108 a
JOIN huge_table_1108_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1109 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1109 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4715'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1110
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1112 a
JOIN huge_table_1112_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1113 a
JOIN huge_table_1113_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1114 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1114 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2187'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1115
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1116 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1116 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1537'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1117 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1117 (user_id, username, password, email)
VALUES (1117, 'user_1117', 'P@ss_6410', 'user_1117@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1120 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1120
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1122
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1123 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1125 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1126 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1126 (user_id, username, password, email)
VALUES (1126, 'user_1126', 'P@ss_4359', 'user_1126@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1127
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1130 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1130 (user_id, username, password, email)
VALUES (1130, 'user_1130', 'P@ss_9815', 'user_1130@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1130
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1131 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1131 (user_id, username, password, email)
VALUES (1131, 'user_1131', 'P@ss_7610', 'user_1131@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1132
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1133
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1135 a
JOIN huge_table_1135_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1136 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1136 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6049'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1137
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1138
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1139 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1140
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1146 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1149 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1149 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9158'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1150 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1150 (user_id, username, password, email)
VALUES (1150, 'user_1150', 'P@ss_7582', 'user_1150@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1150
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1151
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1152 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1153 a
JOIN huge_table_1153_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1154 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1154 (user_id, username, password, email)
VALUES (1154, 'user_1154', 'P@ss_2907', 'user_1154@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1155
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1157 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1157 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5167'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1160 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1160 (user_id, username, password, email)
VALUES (1160, 'user_1160', 'P@ss_4088', 'user_1160@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1160
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1161 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1162
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1163 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1165 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1165 (user_id, username, password, email)
VALUES (1165, 'user_1165', 'P@ss_7439', 'user_1165@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1166 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1166 (user_id, username, password, email)
VALUES (1166, 'user_1166', 'P@ss_6690', 'user_1166@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1169 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1169 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1557'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1170
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1171 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1171 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2025'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1172 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1172 (user_id, username, password, email)
VALUES (1172, 'user_1172', 'P@ss_8829', 'user_1172@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1173 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1175 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1175 (user_id, username, password, email)
VALUES (1175, 'user_1175', 'P@ss_8246', 'user_1175@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1178 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1178 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9634'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1180
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1182 a
JOIN huge_table_1182_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1183 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1183 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5021'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1184 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1184 (user_id, username, password, email)
VALUES (1184, 'user_1184', 'P@ss_7082', 'user_1184@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1186 a
JOIN huge_table_1186_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1187 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1187 (user_id, username, password, email)
VALUES (1187, 'user_1187', 'P@ss_6678', 'user_1187@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1189
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1190
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1191 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1194 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1194 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9221'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1195
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1197 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1197 (user_id, username, password, email)
VALUES (1197, 'user_1197', 'P@ss_1327', 'user_1197@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1198
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1199 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1199 (user_id, username, password, email)
VALUES (1199, 'user_1199', 'P@ss_6333', 'user_1199@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1200
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1201 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1202
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1204
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1205 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1205 (user_id, username, password, email)
VALUES (1205, 'user_1205', 'P@ss_1139', 'user_1205@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1207 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1207 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5394'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1208 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1209 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1209 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6423'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1210 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1210
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1211
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1212 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1212 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9421'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1214 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1215
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1216 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1216 (user_id, username, password, email)
VALUES (1216, 'user_1216', 'P@ss_6398', 'user_1216@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1218 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1218 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6578'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1220
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1221 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1221 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1082'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1222 a
JOIN huge_table_1222_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1223 a
JOIN huge_table_1223_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1224 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1224 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5824'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1225 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1227 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1227 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7046'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1228 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1228 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7576'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1230
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 1230
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1231 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1231 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5766'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1234 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1234 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8579'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1235 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1235 (user_id, username, password, email)
VALUES (1235, 'user_1235', 'P@ss_9223', 'user_1235@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1240 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1240
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1241 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1241 (user_id, username, password, email)
VALUES (1241, 'user_1241', 'P@ss_5327', 'user_1241@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1242 a
JOIN huge_table_1242_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1244 a
JOIN huge_table_1244_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1245 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1245 (user_id, username, password, email)
VALUES (1245, 'user_1245', 'P@ss_2903', 'user_1245@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1246 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1246 (user_id, username, password, email)
VALUES (1246, 'user_1246', 'P@ss_3817', 'user_1246@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1248
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1249
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1250 a
JOIN huge_table_1250_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1250
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1251 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1251 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7648'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1252
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1253 a
JOIN huge_table_1253_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1255
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1256 a
JOIN huge_table_1256_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1257
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1258
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1260 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1260
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1261 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1261 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6838'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1262 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1262 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3025'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1263
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1265 a
JOIN huge_table_1265_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1266 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1266 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7174'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1267 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1267 (user_id, username, password, email)
VALUES (1267, 'user_1267', 'P@ss_3409', 'user_1267@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1270 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1270 (user_id, username, password, email)
VALUES (1270, 'user_1270', 'P@ss_3505', 'user_1270@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1270
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1271 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1272 a
JOIN huge_table_1272_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1275
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1276
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1279 a
JOIN huge_table_1279_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1280 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1280 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5702'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1280
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1281 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1281 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5022'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1282
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1285 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1285 (user_id, username, password, email)
VALUES (1285, 'user_1285', 'P@ss_6254', 'user_1285@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1286 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1286 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5299'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1288 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1288 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7049'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1289 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1289 (user_id, username, password, email)
VALUES (1289, 'user_1289', 'P@ss_4388', 'user_1289@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1290 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1290 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6872'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1290
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1291 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1293 a
JOIN huge_table_1293_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1299 a
JOIN huge_table_1299_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1300 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1300
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1302 a
JOIN huge_table_1302_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1304 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1304 (user_id, username, password, email)
VALUES (1304, 'user_1304', 'P@ss_6548', 'user_1304@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1306 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1307 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1308 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1309 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1310 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1310 (user_id, username, password, email)
VALUES (1310, 'user_1310', 'P@ss_2972', 'user_1310@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1310
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1312 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1312 (user_id, username, password, email)
VALUES (1312, 'user_1312', 'P@ss_2164', 'user_1312@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1313 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1314 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1316 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1316 (user_id, username, password, email)
VALUES (1316, 'user_1316', 'P@ss_9618', 'user_1316@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1318 a
JOIN huge_table_1318_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1320 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1320
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1322 a
JOIN huge_table_1322_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1323
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1324 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1325 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1325 (user_id, username, password, email)
VALUES (1325, 'user_1325', 'P@ss_5926', 'user_1325@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1326 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1326 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8723'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1327 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1327 (user_id, username, password, email)
VALUES (1327, 'user_1327', 'P@ss_6210', 'user_1327@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1328 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1328 (user_id, username, password, email)
VALUES (1328, 'user_1328', 'P@ss_8708', 'user_1328@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1329 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1330 a
JOIN huge_table_1330_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1330
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1331
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1332
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1333
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1335 a
JOIN huge_table_1335_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1336 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1337 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1340
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1342 a
JOIN huge_table_1342_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1343 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1343 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9880'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1345 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1345 (user_id, username, password, email)
VALUES (1345, 'user_1345', 'P@ss_4910', 'user_1345@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1346 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1346 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6291'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1347 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1348 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1348 (user_id, username, password, email)
VALUES (1348, 'user_1348', 'P@ss_5461', 'user_1348@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1349
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1350
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1352 a
JOIN huge_table_1352_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1354 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1354 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1543'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1356
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1357 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1357 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4474'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1358 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1358 (user_id, username, password, email)
VALUES (1358, 'user_1358', 'P@ss_5400', 'user_1358@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1360 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1360 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4125'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1360
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1361
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1364 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1365 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1365 (user_id, username, password, email)
VALUES (1365, 'user_1365', 'P@ss_6503', 'user_1365@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1366
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1367 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1369 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1369 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6684'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1370 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1370 (user_id, username, password, email)
VALUES (1370, 'user_1370', 'P@ss_8576', 'user_1370@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1370
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1372 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1373 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1374 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1374 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1554'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1377
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1380
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1381 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1383 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1384 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1384 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6957'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1385
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1388 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1389 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1390
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1392 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1394 a
JOIN huge_table_1394_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1395 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1400 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1400
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1402 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1402 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1910'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1404 a
JOIN huge_table_1404_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1405 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1406 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1406 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1588'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1407 a
JOIN huge_table_1407_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1409 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1409 (user_id, username, password, email)
VALUES (1409, 'user_1409', 'P@ss_3986', 'user_1409@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1410
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1411 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1411 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5935'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1413 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1413 (user_id, username, password, email)
VALUES (1413, 'user_1413', 'P@ss_9045', 'user_1413@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1414 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1414 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2258'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1416
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1417 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1417 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3328'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1418
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1419 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1419 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4951'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1420 a
JOIN huge_table_1420_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1420
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1421 a
JOIN huge_table_1421_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1422 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1422 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2936'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1426
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1427 a
JOIN huge_table_1427_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1428 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1430
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1432 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1432 (user_id, username, password, email)
VALUES (1432, 'user_1432', 'P@ss_8372', 'user_1432@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1433
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1435 a
JOIN huge_table_1435_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1436 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1436 (user_id, username, password, email)
VALUES (1436, 'user_1436', 'P@ss_4559', 'user_1436@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1437 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1438 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1438 (user_id, username, password, email)
VALUES (1438, 'user_1438', 'P@ss_5757', 'user_1438@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1440
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1441 a
JOIN huge_table_1441_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1442 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1442 (user_id, username, password, email)
VALUES (1442, 'user_1442', 'P@ss_6779', 'user_1442@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1444 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1445 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1445 (user_id, username, password, email)
VALUES (1445, 'user_1445', 'P@ss_6160', 'user_1445@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1446 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1446 (user_id, username, password, email)
VALUES (1446, 'user_1446', 'P@ss_8215', 'user_1446@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1447 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1447 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3888'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1450 a
JOIN huge_table_1450_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1450
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1451
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1454 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1454 (user_id, username, password, email)
VALUES (1454, 'user_1454', 'P@ss_4735', 'user_1454@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1455 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1455 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7062'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1458 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1458 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6664'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1459
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1460 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1460 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7048'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1460
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1462 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1462 (user_id, username, password, email)
VALUES (1462, 'user_1462', 'P@ss_6920', 'user_1462@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1464 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1464 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8500'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1466
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1468
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1469 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1469 (user_id, username, password, email)
VALUES (1469, 'user_1469', 'P@ss_6357', 'user_1469@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1470
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1472
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1473
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1477 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1479 a
JOIN huge_table_1479_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1480 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1480 (user_id, username, password, email)
VALUES (1480, 'user_1480', 'P@ss_6711', 'user_1480@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1480
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1481 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1483 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1483 (user_id, username, password, email)
VALUES (1483, 'user_1483', 'P@ss_3762', 'user_1483@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1484 a
JOIN huge_table_1484_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1488 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1488 (user_id, username, password, email)
VALUES (1488, 'user_1488', 'P@ss_3195', 'user_1488@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1490 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1490 (user_id, username, password, email)
VALUES (1490, 'user_1490', 'P@ss_1340', 'user_1490@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1490
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1491
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1493 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1493 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4936'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1494 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1496 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1496 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7660'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1500
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1501 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1502
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1505 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1505 (user_id, username, password, email)
VALUES (1505, 'user_1505', 'P@ss_4544', 'user_1505@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1507 a
JOIN huge_table_1507_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1510
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1513
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1515 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1515 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7683'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1516 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1517 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1517 (user_id, username, password, email)
VALUES (1517, 'user_1517', 'P@ss_6434', 'user_1517@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1518 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1518 (user_id, username, password, email)
VALUES (1518, 'user_1518', 'P@ss_9678', 'user_1518@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1520 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1520
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1521 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1521 (user_id, username, password, email)
VALUES (1521, 'user_1521', 'P@ss_7124', 'user_1521@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1524 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1525 a
JOIN huge_table_1525_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1529 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1529 (user_id, username, password, email)
VALUES (1529, 'user_1529', 'P@ss_5142', 'user_1529@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1530
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 1530
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1531
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1532 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1532 (user_id, username, password, email)
VALUES (1532, 'user_1532', 'P@ss_5032', 'user_1532@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1533 a
JOIN huge_table_1533_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1534 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1534 (user_id, username, password, email)
VALUES (1534, 'user_1534', 'P@ss_9652', 'user_1534@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1535 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1535 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4626'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1536 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1536 (user_id, username, password, email)
VALUES (1536, 'user_1536', 'P@ss_8414', 'user_1536@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1537
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1538
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1539 a
JOIN huge_table_1539_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1540
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1541 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1541 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7389'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1543 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1546 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1546 (user_id, username, password, email)
VALUES (1546, 'user_1546', 'P@ss_4847', 'user_1546@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1547 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1547 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4244'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1548 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1549 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1549 (user_id, username, password, email)
VALUES (1549, 'user_1549', 'P@ss_8344', 'user_1549@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1550
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1552 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1553 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1553 (user_id, username, password, email)
VALUES (1553, 'user_1553', 'P@ss_4224', 'user_1553@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1554 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1557 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1557 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6960'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1558
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1559 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1559 (user_id, username, password, email)
VALUES (1559, 'user_1559', 'P@ss_8309', 'user_1559@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1560
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1563 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1566
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1567 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1567 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6643'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1569 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1569 (user_id, username, password, email)
VALUES (1569, 'user_1569', 'P@ss_4068', 'user_1569@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1570 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1570 (user_id, username, password, email)
VALUES (1570, 'user_1570', 'P@ss_2968', 'user_1570@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1570
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1575 a
JOIN huge_table_1575_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1577 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1577 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9794'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1578 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1579 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1580 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1580
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1581 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1581 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4915'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1582 a
JOIN huge_table_1582_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1583 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1584 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1584 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1250'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1586 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1586 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2072'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1588 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1588 (user_id, username, password, email)
VALUES (1588, 'user_1588', 'P@ss_7669', 'user_1588@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1590 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1590
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1592 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1592 (user_id, username, password, email)
VALUES (1592, 'user_1592', 'P@ss_5731', 'user_1592@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1593 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1593 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3021'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1594 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1594 (user_id, username, password, email)
VALUES (1594, 'user_1594', 'P@ss_1344', 'user_1594@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1596 a
JOIN huge_table_1596_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1597
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1600
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1601 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1601 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5861'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1602
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1604
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1605 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1606
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1608 a
JOIN huge_table_1608_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1610 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1610 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6149'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1610
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1611 a
JOIN huge_table_1611_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1612 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1612 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6682'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1613 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1613 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6681'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1615 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1615 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3416'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1620 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1620
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1623 a
JOIN huge_table_1623_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1624 a
JOIN huge_table_1624_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1628
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1629 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1629 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8954'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1630
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 1630
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1631 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1632 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1632 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6488'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1633 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1634 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1634 (user_id, username, password, email)
VALUES (1634, 'user_1634', 'P@ss_7827', 'user_1634@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1636 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1636 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4072'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1640 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1640
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1642
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1643
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1645 a
JOIN huge_table_1645_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1646 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1646 (user_id, username, password, email)
VALUES (1646, 'user_1646', 'P@ss_9087', 'user_1646@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1648 a
JOIN huge_table_1648_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1649 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1649 (user_id, username, password, email)
VALUES (1649, 'user_1649', 'P@ss_3562', 'user_1649@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1650
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1651 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1651 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4615'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1652 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1652 (user_id, username, password, email)
VALUES (1652, 'user_1652', 'P@ss_2917', 'user_1652@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1654 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1654 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7746'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1656 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1656 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5701'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1657 a
JOIN huge_table_1657_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1659 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1659 (user_id, username, password, email)
VALUES (1659, 'user_1659', 'P@ss_7667', 'user_1659@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1660
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1663 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1663 (user_id, username, password, email)
VALUES (1663, 'user_1663', 'P@ss_3591', 'user_1663@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1665 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1665 (user_id, username, password, email)
VALUES (1665, 'user_1665', 'P@ss_3991', 'user_1665@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1666 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1666 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6583'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1668 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1669 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1669 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3333'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1670 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1670
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1673
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1674
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1676 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1677 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1677 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5216'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1678 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1679 a
JOIN huge_table_1679_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1680
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 1680
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1681
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1682 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1682 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3180'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1684 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1684 (user_id, username, password, email)
VALUES (1684, 'user_1684', 'P@ss_7293', 'user_1684@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1685 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1687 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1688 a
JOIN huge_table_1688_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1689 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1689 (user_id, username, password, email)
VALUES (1689, 'user_1689', 'P@ss_2356', 'user_1689@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1690
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1691
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1692 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1692 (user_id, username, password, email)
VALUES (1692, 'user_1692', 'P@ss_5879', 'user_1692@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1693 a
JOIN huge_table_1693_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1694 a
JOIN huge_table_1694_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1695
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1696
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1700 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1700
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1701 a
JOIN huge_table_1701_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1702 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1702 (user_id, username, password, email)
VALUES (1702, 'user_1702', 'P@ss_2840', 'user_1702@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1704
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1707 a
JOIN huge_table_1707_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1710 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1710 (user_id, username, password, email)
VALUES (1710, 'user_1710', 'P@ss_8694', 'user_1710@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1710
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1713 a
JOIN huge_table_1713_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1716
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1717 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1717 (user_id, username, password, email)
VALUES (1717, 'user_1717', 'P@ss_4519', 'user_1717@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1718 a
JOIN huge_table_1718_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1719
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1720
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1722
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1725 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1727
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1728
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1729 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1729 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7344'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1730
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1732 a
JOIN huge_table_1732_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1733 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1734 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1734 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4368'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1736 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1737 a
JOIN huge_table_1737_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1738
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1740 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1740 (user_id, username, password, email)
VALUES (1740, 'user_1740', 'P@ss_4936', 'user_1740@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1740
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1741
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1742 a
JOIN huge_table_1742_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1743 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1743 (user_id, username, password, email)
VALUES (1743, 'user_1743', 'P@ss_3198', 'user_1743@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1744 a
JOIN huge_table_1744_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1745 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1745 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3022'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1746 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1746 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9629'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1749
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1750 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1750
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1753 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1753 (user_id, username, password, email)
VALUES (1753, 'user_1753', 'P@ss_4238', 'user_1753@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1754 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1754 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8399'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1756 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1756 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1716'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1757 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1757 (user_id, username, password, email)
VALUES (1757, 'user_1757', 'P@ss_4550', 'user_1757@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1758
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1759
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1760 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1760 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2003'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1760
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1763 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1763 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6391'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1764 a
JOIN huge_table_1764_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1765 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1765 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3145'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1767 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1767 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5901'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1769
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1770 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1770
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1771 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1771 (user_id, username, password, email)
VALUES (1771, 'user_1771', 'P@ss_5033', 'user_1771@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1772 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1773 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1773 (user_id, username, password, email)
VALUES (1773, 'user_1773', 'P@ss_2619', 'user_1773@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1775 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1777 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1777 (user_id, username, password, email)
VALUES (1777, 'user_1777', 'P@ss_5751', 'user_1777@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1778 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1778 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2370'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1780 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1780
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1781 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1781 (user_id, username, password, email)
VALUES (1781, 'user_1781', 'P@ss_5414', 'user_1781@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1782
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1784
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1785 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1786 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1786 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9972'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1787 a
JOIN huge_table_1787_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1788 a
JOIN huge_table_1788_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1789 a
JOIN huge_table_1789_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1790
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1791 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1791 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_4696'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1792 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1792 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3427'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1793
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1795 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1795 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7999'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1797 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1797 (user_id, username, password, email)
VALUES (1797, 'user_1797', 'P@ss_7329', 'user_1797@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1799 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1799 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_8437'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1800 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1800 (user_id, username, password, email)
VALUES (1800, 'user_1800', 'P@ss_9695', 'user_1800@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1800
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1801 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1801 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9591'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1802 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1802 (user_id, username, password, email)
VALUES (1802, 'user_1802', 'P@ss_8928', 'user_1802@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1803 a
JOIN huge_table_1803_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1804 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1804 (user_id, username, password, email)
VALUES (1804, 'user_1804', 'P@ss_2336', 'user_1804@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1806 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1806 (user_id, username, password, email)
VALUES (1806, 'user_1806', 'P@ss_6857', 'user_1806@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1807 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1807 (user_id, username, password, email)
VALUES (1807, 'user_1807', 'P@ss_1305', 'user_1807@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1808
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1810
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1811 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1813
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1814
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1815 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1816 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1819 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1819 (user_id, username, password, email)
VALUES (1819, 'user_1819', 'P@ss_6633', 'user_1819@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1820
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1821 a
JOIN huge_table_1821_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1822
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1823 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1823 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7956'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1825 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1825 (user_id, username, password, email)
VALUES (1825, 'user_1825', 'P@ss_3350', 'user_1825@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1826 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1826 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3745'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1828 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1829 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1829 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5651'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1830 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1830
SELECT 1;

-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1832 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1832 (user_id, username, password, email)
VALUES (1832, 'user_1832', 'P@ss_5038', 'user_1832@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1834 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1834 (user_id, username, password, email)
VALUES (1834, 'user_1834', 'P@ss_9429', 'user_1834@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1835 a
JOIN huge_table_1835_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1836 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1836 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7118'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1840
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====


-- benign comment block 1840
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1841 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1841 (user_id, username, password, email)
VALUES (1841, 'user_1841', 'P@ss_5569', 'user_1841@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1843 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1843 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9571'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1848 a
JOIN huge_table_1848_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


-- benign comment block 1850
SELECT 1;

-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1851 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1851 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1320'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1852 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1853
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1854 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1854 (user_id, username, password, email)
VALUES (1854, 'user_1854', 'P@ss_4892', 'user_1854@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1855
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1858 a
JOIN huge_table_1858_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1859
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1860 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1860 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9224'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1860
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1861 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1862 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1864 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1865 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1865 (user_id, username, password, email)
VALUES (1865, 'user_1865', 'P@ss_3855', 'user_1865@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1867
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1868 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1868 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9788'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1870
SELECT 1;

-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1871 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1871 (user_id, username, password, email)
VALUES (1871, 'user_1871', 'P@ss_1339', 'user_1871@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1872 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1872 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2695'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1874 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1876
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1879
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1880 a
JOIN huge_table_1880_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1880
SELECT 1;

-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1881 a
JOIN huge_table_1881_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1882 a
JOIN huge_table_1882_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1885 a
JOIN huge_table_1885_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1886 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1886 (user_id, username, password, email)
VALUES (1886, 'user_1886', 'P@ss_8809', 'user_1886@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1887 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1888 a
JOIN huge_table_1888_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1890 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1890 (user_id, username, password, email)
VALUES (1890, 'user_1890', 'P@ss_8188', 'user_1890@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====


-- benign comment block 1890
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1891
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1892 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1892 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6639'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1893 a
JOIN huge_table_1893_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1894 a
JOIN huge_table_1894_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1895
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1896
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1898 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1898 (user_id, username, password, email)
VALUES (1898, 'user_1898', 'P@ss_3667', 'user_1898@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1899 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1899 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7496'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1900 a
JOIN huge_table_1900_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1900
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1902 a
JOIN huge_table_1902_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1903
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1904 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1904 (user_id, username, password, email)
VALUES (1904, 'user_1904', 'P@ss_7029', 'user_1904@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1906 a
JOIN huge_table_1906_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1907 a
JOIN huge_table_1907_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1910 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====


-- benign comment block 1910
SELECT 1;

-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1913 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1913 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7073'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1914 a
JOIN huge_table_1914_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1917 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1917 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_1036'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1918 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1918 (user_id, username, password, email)
VALUES (1918, 'user_1918', 'P@ss_5723', 'user_1918@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====


-- benign comment block 1920
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1921 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1922 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1923 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1924 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1926 a
JOIN huge_table_1926_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1930 a
JOIN huge_table_1930_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1930
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1931
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1932 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1933 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1933 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_6388'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1935 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1936 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1938
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1939 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1940 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1940 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_7810'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1940
SELECT 1;

-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1943 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1943 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5384'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1944
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1945
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1946 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1946 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_3686'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1947 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1947 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_5705'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====


-- benign comment block 1950
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1951 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1952 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1952 (user_id, username, password, email)
VALUES (1952, 'user_1952', 'P@ss_4740', 'user_1952@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1953 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1953 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_2242'); -- CRITICAL: credential in code
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1956 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1957 a
JOIN huge_table_1957_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: AGGREGATION BUG (CRITICAL) =====
SELECT e.employee_id, e.first_name, e.last_name, COUNT(t.task_id) AS total_tasks,
    SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) AS completed_tasks,
    (SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END) / COUNT(t.task_id)) * 100 AS completion_rate
FROM employees e
LEFT JOIN tasks t ON e.employee_id = t.employee_id
WHERE e.active = 1
GROUP BY e.employee_id
HAVING completion_rate > 80; -- CRITICAL: alias used in HAVING (not allowed in many dialects)
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1959
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: CREDENTIALS TABLE (CRITICAL) =====
CREATE TABLE app_config_1960 (
    cfg_key VARCHAR(200) PRIMARY KEY,
    cfg_value VARCHAR(200)
);

INSERT INTO app_config_1960 (cfg_key, cfg_value) VALUES
  ('db_user', 'app_user'),
  ('db_pass', 'SuperSecret_9520'); -- CRITICAL: credential in code
-- ===== END BLOCK =====


-- benign comment block 1960
SELECT 1;

-- ===== BLOCK: REPORT EXPOSING PASSWORD (CRITICAL/HIGH) =====
SELECT u.username, u.password, SUM(o.amount) AS total_spent, COUNT(o.order_id) AS order_count
FROM bad_users_1961 u
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_date BETWEEN '2015-01-01' AND '2024-12-31' -- HIGH: huge hardcoded date range
GROUP BY u.username; -- CRITICAL: missing u.password in GROUP BY but selected
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1962
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1963 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1963 (user_id, username, password, email)
VALUES (1963, 'user_1963', 'P@ss_5424', 'user_1963@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1964 a
JOIN huge_table_1964_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1966 a
JOIN huge_table_1966_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1967 a
JOIN huge_table_1967_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====



-- ===== BLOCK: HUGE LIMIT (HIGH/MEDIUM) =====
SELECT u.user_id, u.username, o.order_id, o.amount
FROM users u
JOIN orders o ON u.user_id = o.user_id
ORDER BY o.amount DESC
LIMIT 1000000; -- HIGH: absurdly large limit, performance problem
-- ===== END BLOCK =====



-- ===== BLOCK: USER CREATION (CRITICAL) =====
CREATE TABLE bad_users_1969 (
    user_id INT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) DEFAULT 'DefaultPass123!', -- CRITICAL: default plain password
    email VARCHAR(200)
);

INSERT INTO bad_users_1969 (user_id, username, password, email)
VALUES (1969, 'user_1969', 'P@ss_7557', 'user_1969@example.com'); -- CRITICAL: hardcoded plain password
-- ===== END BLOCK =====



-- ===== BLOCK: HEAVY JOIN WITHOUT INDEX (MEDIUM/HIGH) =====
SELECT a.*, b.*
FROM huge_table_1970 a
JOIN huge_table_1970_b b ON a.join_col = b.join_col
WHERE a.event_date >= '2022-01-01';
-- MEDIUM: no indexes mentioned; will cause full scans on huge tables
-- ===== END BLOCK =====


-- benign comment block 1970
SELECT 1;

-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1971
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: AMBIGUOUS COLUMNS (MEDIUM) =====
SELECT id, name, created_at
FROM public_schema.sample_table_1972
WHERE status = 'active';
-- MEDIUM: no table alias used; ambiguity risk if joined later
-- ===== END BLOCK =====



-- ===== BLOCK: LEFT JOIN FILTER BUG (HIGH) =====
SELECT i.item_id, i.item_name, s.supplier_name, AVG(p.purchase_price) AS avg_price
FROM inventory i
LEFT JOIN purchases p ON i.item_id = p.item_id
JOIN suppliers s ON i.supplier_id = s.supplier_id
WHERE p.purchase_date >= '2023-01-01' -- HIGH: filters null purchases, makes LEFT JOIN useless
GROUP BY i.item_id, i.item_name, s.supplier_name;
-- ===== END BLOCK =====


