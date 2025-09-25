
-- test_small.sql
-- Small SQL file to trigger a critical dynamic-SQL finding.
-- CRITICAL: dynamic SQL using concatenation of untrusted input.

CREATE TABLE IF NOT EXISTS users (
  id serial PRIMARY KEY,
  name text
);

-- Vulnerable function: builds SQL by concatenation and executes it.
CREATE OR REPLACE FUNCTION get_user_info(username text)
RETURNS SETOF users AS $$
BEGIN
  -- Unsafe: concatenates username into SQL string and EXECUTEs it
  RETURN QUERY EXECUTE 'SELECT * FROM users WHERE name = ''' || username || '''';
END;
$$ LANGUAGE plpgsql;
