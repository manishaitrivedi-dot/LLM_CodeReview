-- sql_dynamic_pg.sql
-- CRITICAL: dynamic EXECUTE with concatenated user input (SQL injection)

CREATE TABLE IF NOT EXISTS users (
  id serial PRIMARY KEY,
  name text
);

CREATE OR REPLACE FUNCTION get_user_info(username text)
RETURNS SETOF users AS $$
BEGIN
  -- Unsafe: concatenates username and executes it
  RETURN QUERY EXECUTE 'SELECT * FROM users WHERE name = ''' || username || '''';
END;
$$ LANGUAGE plpgsql;
