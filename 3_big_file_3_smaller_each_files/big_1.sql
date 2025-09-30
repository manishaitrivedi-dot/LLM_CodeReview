-- auto-generated large SQL for testing
-- contains many functions with dynamic SQL and concatenations


-- Function A: get_data_A_0001
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0001(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0001*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0002
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0002(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0002*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0003
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0003(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0003*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0004
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0004(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0004*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0005
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0005(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0005*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0006
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0006(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0006*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0007
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0007(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0007*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0008
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0008(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0008*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0009
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0009(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0009*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0010
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0010(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0010*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0011
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0011(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0011*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0012
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0012(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0012*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0013
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0013(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0013*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0014
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0014(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0014*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0015
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0015(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0015*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0016
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0016(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0016*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0017
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0017(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0017*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0018
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0018(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0018*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0019
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0019(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0019*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0020
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0020(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0020*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0021
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0021(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0021*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0022
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0022(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0022*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0023
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0023(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0023*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0024
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0024(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0024*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0025
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0025(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0025*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0026
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0026(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0026*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0027
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0027(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0027*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0028
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0028(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0028*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0029
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0029(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0029*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0030
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0030(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0030*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0031
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0031(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0031*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0032
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0032(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0032*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0033
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0033(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0033*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0034
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0034(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0034*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0035
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0035(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0035*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0036
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0036(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0036*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0037
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0037(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0037*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0038
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0038(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0038*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0039
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0039(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0039*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0040
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0040(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0040*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0041
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0041(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0041*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0042
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0042(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0042*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0043
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0043(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0043*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0044
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0044(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0044*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0045
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0045(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0045*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0046
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0046(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0046*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0047
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0047(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0047*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0048
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0048(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0048*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0049
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0049(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0049*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0050
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0050(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0050*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0051
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0051(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0051*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0052
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0052(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0052*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0053
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0053(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0053*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0054
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0054(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0054*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0055
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0055(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0055*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0056
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0056(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0056*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0057
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0057(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0057*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0058
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0058(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0058*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0059
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0059(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0059*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0060
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0060(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0060*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0061
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0061(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0061*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0062
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0062(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0062*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0063
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0063(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0063*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0064
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0064(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0064*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0065
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0065(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0065*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0066
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0066(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0066*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0067
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0067(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0067*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0068
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0068(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0068*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0069
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0069(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0069*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0070
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0070(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0070*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0071
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0071(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0071*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0072
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0072(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0072*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0073
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0073(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0073*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0074
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0074(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0074*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0075
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0075(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0075*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0076
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0076(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0076*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0077
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0077(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0077*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0078
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0078(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0078*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0079
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0079(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0079*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0080
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0080(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0080*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0081
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0081(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0081*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0082
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0082(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0082*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0083
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0083(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0083*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0084
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0084(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0084*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0085
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0085(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0085*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0086
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0086(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*a:0086*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0087
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0087(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;

  qry := qry || ' /*a:0087*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0088
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0088(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;

  qry := qry || ' /*a:0088*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0089
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0089(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;
  IF (k % 11) = 10 THEN qry := qry || ' AND meta->>''key10'' = ''val10'''; END IF; k := k + 1;
  IF (k % 12) = 11 THEN qry := qry || ' AND meta->>''key11'' = ''val11'''; END IF; k := k + 1;
  IF (k % 13) = 12 THEN qry := qry || ' AND meta->>''key12'' = ''val12'''; END IF; k := k + 1;

  qry := qry || ' /*a:0089*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0090
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0090(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*a:0090*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function A: get_data_A_0091
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_A_0091(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  k integer := 0;
BEGIN
  qry := 'SELECT id, name, email FROM users WHERE name = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*a:0091*/' || repeat('A', 25);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);
