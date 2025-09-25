def main(session, check_ids, email_int_name, task_name):
    # imports
    import pandas as pd
    import logging
    from datetime import datetime
    from ast import literal_eval
    from snowflake.snowpark import functions
    from snowflake.snowpark.functions import asc, check_json, check_xml, col, contains, count, current_timestamp, desc, lit, length, expr
    logger = logging.Logger("DQ Sproc")
    
    ########################
    ##### Unique check #####
    ########################
    def unique_check(row, table_dict, session, current_ts):
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        unique_check = table_df.groupBy(col(f'"{column_name}"')).count().filter(col("count") > 1)
        if unique_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            duplicate_rows = table_df.join(unique_check, on=f'"{column_name}"', how="inner").withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('UNIQUE_CHECK')).withColumn('INPUT_PARAMS',lit('')).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'UNIQUE_CHECK'").collect()
            duplicate_rows.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"update data_quality_checks set result = '{result}', last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'unique_check'").collect()
            return [check_id, database_name, schema_name, table_name, column_name, "Unique check", None]
        else:
            result = "PASS"
            session.sql(f"update data_quality_checks set result = '{result}', last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'unique_check'").collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'UNIQUE_CHECK'").collect()
            return []

    ######################
    ##### Null check #####
    ######################
    def null_check(row, table_dict, session, current_ts):
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        null_check = table_df.where(col(f'"{column_name}"').isNull())
        if null_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            null_check = null_check.withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('NULL_CHECK')).withColumn('INPUT_PARAMS',lit('')).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'NULL_CHECK'").collect()
            null_check.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'null_check'").collect()
            return [check_id, database_name, schema_name, table_name, column_name, "NULL check", None]
        else:
            result = "PASS"
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}'and check_name = 'null_check'").collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'NULL_CHECK'").collect()
            return []
        
        
    ######################
    ##### Json check #####
    ######################  
    def json_check(row, table_dict, session, current_ts):
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        json_check = table_df.select(col(f'"{column_name}"'),check_json(f'"{column_name}"').alias("JSON_CHECK")).where(col("JSON_CHECK").isNotNull())
        if json_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            json_check = json_check.withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('JSON_CHECK')).withColumn('INPUT_PARAMS',lit('')).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'JSON_CHECK'").collect()
            json_check.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'json_check'").collect()
            return [check_id, database_name, schema_name, table_name, column_name, "JSON check", None]
        else:
            result = "PASS"
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'json_check'").collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'JSON_CHECK'").collect()
            return []
        

    #####################
    ##### XML check #####
    #####################  
    def xml_check(row, table_dict, session, current_ts):
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        xml_check = table_df.select(col(f'"{column_name}"'),check_xml(f'"{column_name}"').alias("XML_CHECK")).where(col("XML_CHECK").isNotNull())
        if xml_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            xml_check = xml_check.withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('XML_CHECK')).withColumn('INPUT_PARAMS',lit('')).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'XML_CHECK'").collect()
            xml_check.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'xml_check'").collect()
            return [check_id, database_name, schema_name, table_name, column_name, "XML check", None]
        else:
            result = "PASS"
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'xml_check'").collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'XML_CHECK'").collect()
            return []
        

    ########################
    ##### Length check #####
    ########################   
    def length_check(row, table_dict, session, current_ts):
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        max_permissible_length=row[7]
        # validate input param
        if not isinstance(max_permissible_length,(str,int)):
            raise Exception(f'max_permissible_length parameter should be a string or integer, not {type(max_permissible_length)}')
        max_permissible_length = int(float(max_permissible_length)) if isinstance(max_permissible_length, str) else max_permissible_length
        
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        # length check logic
        length_check = table_df.filter(length(col(f'"{column_name}"')) > lit(max_permissible_length))
        
        if length_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            length_check = length_check.withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('LENGTH_CHECK')).withColumn('INPUT_PARAMS',lit(row[7])).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'LENGTH_CHECK'").collect()
            length_check.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'length_check' and input_parameter = '{row[7]}'").collect()
            return [check_id, database_name, schema_name, table_name, column_name, "Length check",max_permissible_length]
        else:
            result = "PASS"
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'length_check' and input_parameter = '{row[7]}'").collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'LENGTH_CHECK'").collect()
            return []
        

    ##############################
    ##### Valid_values check #####
    ##############################
    def valid_values_check(row, table_dict, session, current_ts):
        # pre-defined list of sql types
        SQL_STRING_TYPES = ["char","character","varchar","text","string"]
        SQL_INT_TYPES = ["number","bigint","tinyint","smallint","int","integer","hugeint"]
        SQL_FLOAT_TYPES = ["decimal","dec","numeric","number","real","float","double","double precision"]
        SQL_DATE_TYPES = ["date"]
        SQL_TIME_TYPES = ["time"]
        SQL_TIMESTAMP_TYPES = ["datetime","timestamp","timestamp_ltz","timestamp_ntz","timestamp_tz"]
        
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        valid_values_list=row[7]
        
        # validate input param
        if not isinstance(valid_values_list,(str,list)):
            raise Exception(f'valid_values_list parameter should be a string or list, not {type(valid_values_list)}')
        valid_values_list = literal_eval(valid_values_list) if isinstance(valid_values_list, str) else valid_values_list
        
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        # validating inputs based on dtype of column
        dtypes_dict = table_df.dtypes
        for column, dtype in dtypes_dict:
            if column.replace('"','') == column_name:
                if '(' in dtype:
                    dtype=dtype.split('(')[0]
                    if dtype.lower() in SQL_STRING_TYPES:
                        valid_values_list = [str(i) for i in valid_values_list]
                    elif dtype.lower() in SQL_INT_TYPES:
                        valid_values_list = [int(i) for i in valid_values_list]
                    elif dtype.lower() in SQL_FLOAT_TYPES:
                        valid_values_list = [float(i) for i in valid_values_list]
                    elif dtype.lower()  in SQL_DATE_TYPES:
                        valid_values_list = [datetime.strptime(i, '%Y-%m-%d') for i in valid_values_list]
                    elif dtype.lower()  in SQL_TIME_TYPES:
                        valid_values_list = [datetime.strptime(i, '%H:%M:%S') for i in valid_values_list]
                    elif dtype.lower()  in SQL_TIMESTAMP_TYPES:
                        valid_values_list = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in valid_values_list]
                else:
                    if dtype.lower() in SQL_STRING_TYPES:
                        valid_values_list = [str(i) for i in valid_values_list]
                    elif dtype.lower() in SQL_INT_TYPES:
                        valid_values_list = [int(i) for i in valid_values_list]
                    elif dtype.lower() in SQL_FLOAT_TYPES:
                        valid_values_list = [float(i) for i in valid_values_list]
                    elif dtype.lower()  in SQL_DATE_TYPES:
                        valid_values_list = [datetime.strptime(i, '%Y-%m-%d') for i in valid_values_list]
                    elif dtype.lower()  in SQL_TIME_TYPES:
                        valid_values_list = [datetime.strptime(i, '%H:%M:%S') for i in valid_values_list]
                    elif dtype.lower()  in SQL_TIMESTAMP_TYPES:
                        valid_values_list = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in valid_values_list]
        # valid values logic
        valid_values_check = table_df.filter(~col(f'"{column_name}"').isin(valid_values_list))
        if valid_values_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            valid_values_check = valid_values_check.withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('VALID_VALUES_CHECK')).withColumn('INPUT_PARAMS',lit(row[7])).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'VALID_VALUES_CHECK'").collect()
            valid_values_check.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"""update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'valid_values_check' """).collect()
            return [check_id, database_name, schema_name, table_name, column_name, "Valid values check",valid_values_list]
        else:
            result = "PASS"
            session.sql(f"""update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'valid_values_check' """).collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'VALID_VALUES_CHECK'").collect()
            return []
        

    #######################
    ##### Range check #####
    #######################
    def range_check(row, table_dict, session, current_ts):
        # pre-defined list of sql types
        SQL_STRING_TYPES = ["char","character","varchar","text","string"]
        SQL_INT_TYPES = ["number","bigint","tinyint","smallint","int","integer","hugeint"]
        SQL_FLOAT_TYPES = ["decimal","dec","numeric","number","real","float","double","double precision"]
        SQL_DATE_TYPES = ["date"]
        SQL_TIME_TYPES = ["time"]
        SQL_TIMESTAMP_TYPES = ["datetime","timestamp","timestamp_ltz","timestamp_ntz","timestamp_tz"]
        
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        range_list=row[7]
        
        # validate input param
        if not isinstance(range_list,(str,list)):
            raise Exception(f'range_list parameter should be a string or list, not {type(range_list)}')
        range_list = literal_eval(range_list) if isinstance(range_list, str) else range_list
        
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        dtypes_dict = table_df.dtypes
        for column, dtype in dtypes_dict:
            if column.replace('"','') == column_name:
                if '(' in dtype:
                    dtype=dtype.split('(')[0]
                    if dtype.lower() in SQL_STRING_TYPES:
                        range_list = [str(i) for i in range_list]
                    elif dtype.lower() in SQL_INT_TYPES:
                        range_list = [int(i) for i in range_list]
                    elif dtype.lower() in SQL_FLOAT_TYPES:
                        range_list = [float(i) for i in range_list]
                    elif dtype.lower()  in SQL_DATE_TYPES:
                        valid_values_list = [datetime.strptime(i, '%Y-%m-%d') for i in range_list]
                    elif dtype.lower()  in SQL_TIME_TYPES:
                        valid_values_list = [datetime.strptime(i, '%H:%M:%S') for i in range_list]
                    elif dtype.lower()  in SQL_TIMESTAMP_TYPES:
                        valid_values_list = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in range_list]
                else:
                    if dtype.lower() in SQL_STRING_TYPES:
                        range_list = [str(i) for i in range_list]
                    elif dtype.lower() in SQL_INT_TYPES:
                        range_list = [int(i) for i in range_list]
                    elif dtype.lower() in SQL_FLOAT_TYPES:
                        range_list = [float(i) for i in range_list]
                    elif dtype.lower()  in SQL_DATE_TYPES:
                        valid_values_list = [datetime.strptime(i, '%Y-%m-%d') for i in range_list]
                    elif dtype.lower()  in SQL_TIME_TYPES:
                        valid_values_list = [datetime.strptime(i, '%H:%M:%S') for i in range_list]
                    elif dtype.lower()  in SQL_TIMESTAMP_TYPES:
                        valid_values_list = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in range_list]
        
        # range check logic
        range_check = table_df.filter(~((col(f'"{column_name}"') >= range_list[0]) & (col(f'"{column_name}"') <= range_list[1])))
        
        if range_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            range_check = range_check.withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('RANGE_CHECK')).withColumn('INPUT_PARAMS',lit(row[7])).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'RANGE_CHECK'").collect()
            range_check.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'range_check'").collect()
            return [check_id, database_name, schema_name, table_name, column_name, "Range check",range_list]
        else:
            result = "PASS"
            session.sql(f"update data_quality_checks set result = '{result}',last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'range_check'").collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'RANGE_CHECK'").collect()
            return []
        
    ####################
    ### regexp check ###
    ####################
    def regexp_check(row, table_dict, session, current_ts):
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        reg_expr = row[7]
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        regexp_check = table_df.filter(~col(f'"{column_name}"').rlike(f'{reg_expr}'))
        if regexp_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            regexp_check = regexp_check.withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('REGEXP_CHECK')).withColumn('INPUT_PARAMS',lit(reg_expr)).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'REGEXP_CHECK'").collect()
            regexp_check.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"update data_quality_checks set result = '{result}', last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'regexp_check'").collect()
            return [check_id, database_name, schema_name, table_name, column_name, "RegExp check",reg_expr]
        else:
            result = "PASS"
            session.sql(f"update data_quality_checks set result = '{result}', last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'regexp_check'").collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'REGEXP_CHECK'").collect()
            return []

    ####################
    ### custom check ###
    ####################
    def custom_check(row, table_dict, session, current_ts):
        check_id = row[0]
        database_name = row[1]
        schema_name = row[2]
        table_name = row[3]
        column_name = row[4]
        custom_expr = row[7]
        table_df = table_dict[database_name+'_'+schema_name+'_'+table_name]
        custom_check = table_df.filter(~expr(custom_expr))
        if custom_check.count() > 0:
            result = "FAIL"
            columns = ['CHECK_ID','DATABASE_NAME','SCHEMA_NAME','TABLE_NAME','COLUMN_NAME','FAILED_RECORDS','CHECK_NAME','INPUT_PARAMS','EXECUTED_DATE']
            # logic to find out the failed records
            custom_check = custom_check.withColumn('CHECK_ID',lit(check_id)).withColumn('DATABASE_NAME',lit(database_name)).withColumn('SCHEMA_NAME',lit(schema_name)).withColumn('TABLE_NAME',lit(table_name)).withColumn('COLUMN_NAME',lit(column_name)).withColumnRenamed(f'"{column_name}"','FAILED_RECORDS').withColumn('CHECK_NAME',lit('CUSTOM_CHECK')).withColumn('INPUT_PARAMS',lit(custom_expr)).withColumn('EXECUTED_DATE',lit(current_timestamp())).select(columns).orderBy(col(f'"{column_name}"'))
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'CUSTOM_CHECK'").collect()
            custom_check.write.mode("append").save_as_table("DATA_QUALITY_FAILED_RECORDS")
            session.sql(f"update data_quality_checks set result = '{result}', last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'custom_check'").collect()
            return [check_id, database_name, schema_name, table_name, column_name, "Custom check",custom_expr]
        else:
            result = "PASS"
            session.sql(f"update data_quality_checks set result = '{result}', last_executed_date = '{current_ts}' where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'custom_check'").collect()
            session.sql(f"delete from DATA_QUALITY_FAILED_RECORDS where check_id = '{check_id}' and database_name = '{database_name}' and schema_name = '{schema_name}' and table_name = '{table_name}' and column_name = '{column_name}' and check_name = 'CUSTOM_CHECK'").collect()
            return []
    
    #####################################
    # Main method execution starts here #
    #####################################
    data_quality_df=session.sql('select * from data_quality_checks').filter(col('"CHECK_ID"').isin(check_ids)).to_pandas()
    
    # Reading all required tables and storing it in a dictionary for further use
    # Logic to read the tables into a dictionary
    # This doesn't work (only reads top 1000 rows)
    table_dict = {}
    unique_df = data_quality_df[['DATABASE_NAME','SCHEMA_NAME','TABLE_NAME']].drop_duplicates()
    for idx, data in unique_df.iterrows():
        fully_qualified_table_name = f'"{data[0]}"."{data[1]}"."{data[2]}"'
        table_dict[data['DATABASE_NAME']+'_'+data['SCHEMA_NAME']+'_'+data['TABLE_NAME']]=session.table(f"""{fully_qualified_table_name}""")

    # creating a dispatch table
    dispatch_table = {
        'unique_check': unique_check,
        'null_check': null_check,
        'json_check': json_check,
        'xml_check': xml_check,
        'length_check': length_check,
        'valid_values_check': valid_values_check,
        'range_check': range_check,
        'regexp_check': regexp_check,
        'custom_check': custom_check
    }

    current_ts = session.sql("select current_timestamp()").collect()[0][0]
    
    result_df = pd.DataFrame(columns=['Check_ID','Database_Name','Schema_Name','Table_Name','Column_Name','Check_Name','Condition'])
    # Iterate over the df and run data qualiy checks
    for idx, data in data_quality_df.iterrows():
        if data['CHECK_NAME'].lower() in dispatch_table:
            #result_list.append(dispatch_table[data['CHECK_NAME'].lower()](data, table_dict, session, current_ts))
            res = dispatch_table[data['CHECK_NAME'].lower()](data, table_dict, session, current_ts)
            if len(res) > 0:
                result_df.loc[len(result_df)] = res

    # Send Error notification via email
    try:
        if email_int_name is not None and email_int_name.lower() != "none":

            html_table = result_df.to_html(index=False)
            
            # Replace default styles with custom styles
            html_table = html_table.replace('class="dataframe"', 'style="border-collapse: collapse; width: 100%; font: normal 12px Arial, sans-serif;"')
            html_table = html_table.replace('<th>', '<th style="background-color: #FF6347; color: white; border: 1px solid #ddd; padding: 8px; text-align: center; font-size: 12px;">')
            html_table = html_table.replace('<td>', '<td style="border: 1px solid #ddd; padding: 8px; text-align: center; font-size: 12px;">')
        
            # Add description and wrap in a complete HTML structure
            html_document = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Data Quality - Error Notification</title>
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        margin: 18px;
                        background-color: #f4f4f9;
                        color: #333;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: auto;
                        padding: 20px;
                        background-color: #fff;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        border-radius: 8px;
                    }}
                    h1 {{
                        font-size: 20px;
                        margin-bottom: 20px;
                        text-align: center;
                        color: #FF6347;
                    }}
                    .description {{
                        font-size: 14px;
                        margin-bottom: 20px;
                        text-align: center;
                        color: #666;
                        font-weight: bold;
                    }}
                    table {{
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #FF6347;
                        color: white;
                    }}
                    tr:nth-child(even) {{
                        background-color: #f9f9f9;
                    }}
                    tr:hover {{
                        background-color: #f1f1f1;
                    }}
                    table caption {{
                        caption-side: bottom;
                        font-size: 12px;
                        color: #777;
                        padding-top: 10px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Data Quality - Error Notification</h1>
                    <p class="description">The below table shows the list of failed data quality checks corresponding to the task: <span style="color: #2629de;">{task_name}</span></p>
                    {html_table}
                    <table>
                        <caption>Note: Please address the data quality issues highlighted above</caption>
                    </table>
                </div>
            </body>
            </html>
            """
            
            # Calling the send_email stored proc
            email_recipients = session.sql(f"select email_recipients from app_instance_task_schema.DATA_QUALITY_EMAIL_INTEGRATIONS where integration_name = '{email_int_name}'").collect()[0][0]
            session.call('SYSTEM$SEND_EMAIL',email_int_name,email_recipients,'Data Quality App Error Notification',html_document, 'text/html')
            return "Success with email notification"
        else:
            return "Success without email notification"
    except Exception as E:
        logger.error(f"Unable to send email notification due to the error : {E}")