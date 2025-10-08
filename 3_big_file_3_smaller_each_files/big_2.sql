-- auto-generated large SQL for testing
-- contains many functions with dynamic SQL and concatenations


-- Function B: get_data_B_0001
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0001(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0001*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0002
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0002(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0002*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0003
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0003(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0003*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0004
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0004(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0004*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0005
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0005(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0005*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0006
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0006(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0006*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0007
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0007(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0007*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0008
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0008(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0008*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0009
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0009(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0009*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0010
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0010(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0010*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0011
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0011(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0011*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0012
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0012(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0012*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0013
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0013(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0013*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0014
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0014(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0014*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0015
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0015(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0015*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0016
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0016(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0016*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0017
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0017(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0017*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0018
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0018(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0018*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0019
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0019(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0019*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0020
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0020(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0020*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0021
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0021(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0021*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0022
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0022(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0022*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0023
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0023(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0023*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0024
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0024(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0024*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0025
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0025(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0025*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0026
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0026(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0026*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0027
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0027(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0027*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0028
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0028(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0028*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0029
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0029(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0029*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0030
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0030(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0030*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0031
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0031(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0031*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0032
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0032(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0032*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0033
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0033(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0033*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0034
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0034(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0034*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0035
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0035(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0035*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0036
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0036(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0036*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0037
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0037(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0037*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0038
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0038(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0038*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0039
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0039(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0039*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0040
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0040(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0040*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0041
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0041(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0041*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0042
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0042(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0042*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0043
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0043(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0043*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0044
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0044(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0044*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0045
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0045(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0045*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0046
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0046(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0046*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0047
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0047(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0047*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0048
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0048(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0048*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0049
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0049(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0049*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0050
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0050(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0050*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0051
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0051(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0051*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0052
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0052(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0052*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0053
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0053(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0053*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0054
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0054(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0054*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0055
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0055(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0055*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0056
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0056(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0056*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0057
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0057(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0057*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0058
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0058(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0058*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0059
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0059(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0059*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0060
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0060(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0060*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0061
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0061(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0061*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0062
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0062(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0062*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0063
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0063(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0063*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0064
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0064(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0064*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0065
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0065(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0065*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0066
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0066(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0066*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0067
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0067(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0067*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0068
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0068(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0068*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0069
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0069(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0069*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0070
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0070(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0070*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0071
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0071(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0071*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0072
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0072(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0072*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0073
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0073(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0073*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0074
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0074(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0074*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0075
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0075(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0075*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0076
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0076(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0076*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0077
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0077(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0077*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0078
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0078(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0078*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0079
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0079(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0079*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0080
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0080(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0080*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0081
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0081(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0081*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0082
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0082(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0082*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0083
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0083(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0083*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0084
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0084(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0084*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0085
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0085(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0085*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0086
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0086(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0086*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0087
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0087(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0087*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0088
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0088(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0088*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0089
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0089(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
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

  qry := qry || ' /*b:0089*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0090
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0090(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;

  qry := qry || ' /*b:0090*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0091
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0091(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;

  qry := qry || ' /*b:0091*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);



-- Function B: get_data_B_0092
-- CRITICAL pattern: dynamic EXECUTE with concatenated user input (SQL injection)
CREATE OR REPLACE FUNCTION get_data_B_0092(param text)
RETURNS SETOF users AS $$
DECLARE
  qry text;
  j integer := 0;
BEGIN
  qry := 'SELECT id, name FROM users WHERE email = ''' || param || '''';
  IF (k % 2) = 1 THEN qry := qry || ' AND meta->>''key1'' = ''val1'''; END IF; k := k + 1;
  IF (k % 3) = 2 THEN qry := qry || ' AND meta->>''key2'' = ''val2'''; END IF; k := k + 1;
  IF (k % 4) = 3 THEN qry := qry || ' AND meta->>''key3'' = ''val3'''; END IF; k := k + 1;
  IF (k % 5) = 4 THEN qry := qry || ' AND meta->>''key4'' = ''val4'''; END IF; k := k + 1;
  IF (k % 6) = 5 THEN qry := qry || ' AND meta->>''key5'' = ''val5'''; END IF; k := k + 1;
  IF (k % 7) = 6 THEN qry := qry || ' AND meta->>''key6'' = ''val6'''; END IF; k := k + 1;
  IF (k % 8) = 7 THEN qry := qry || ' AND meta->>''key7'' = ''val7'''; END IF; k := k + 1;
  IF (k % 9) = 8 THEN qry := qry || ' AND meta->>''key8'' = ''val8'''; END IF; k := k + 1;
  IF (k % 10) = 9 THEN qry := qry || ' AND meta->>''key9'' = ''val9'''; END IF; k := k + 1;

  qry := qry || ' /*b:0092*/' || repeat('B', 30);
  RETURN QUERY EXECUTE qry;
END;
$$ LANGUAGE plpgsql;

SELECT pg_sleep(0.00005);
