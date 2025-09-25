-- sql_concat_table.sql
-- HIGH/MEDIUM: uses concatenated table name (dynamic table access risk)

CREATE OR REPLACE FUNCTION count_rows(table_name text)
RETURNS integer AS $$
DECLARE
  result integer;
BEGIN
  -- concatenating table name into SQL is risky and can be abused
  EXECUTE 'SELECT COUNT(*) FROM ' || table_name INTO result;
  RETURN result;
END;
$$ LANGUAGE plpgsql;
