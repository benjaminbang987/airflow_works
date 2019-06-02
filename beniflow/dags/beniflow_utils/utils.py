""" Utilities file for beniflow project """

import logging
import os
import psycopg2
import pandas as pd
import tempfile
from sqlalchemy import create_engine


def pd_from_sql_wrapper(table_name, schema_name, db_url):
    """
    Wrapper function that takes in table_name, schema_name, db_url and outputs a pandas DataFrame
    """
    with psycopg2.connect(database=db_url) as conn:
        with tempfile.NamedTemporaryFile() as tmpfile:
            query = """
            select * from {schema_name}.{table_name}
            """.format(
                schema_name=schema_name,
                table_name=table_name)
            csv_table_copy = "COPY ({query}) TO STDOUT WITH CSV {header}".format(
                query=query, header="HEADER"
            )
            logging.info("Importing data table from ", schema_name, ".", table_name)
            pd.read_sql()
            connection_cursor = db_url.raw_connection().cursor()
            connection_cursor.copy_expert(csv_table_copy, tmpfile)
            tmpfile.seek(0)
            table_df = pd.read_csv(tmpfile)

    return table_df


def pd_to_sql_wrapper(table_name, schema_name, pandas_df, db_url, db_url_full):
    """
    Wrapper function to speed up pandas.to_sql function
    """
    full_table_name = schema_name + "." + table_name
    db_engine = create_engine(db_url_full)
    with psycopg2.connect(database=db_url) as conn:
        logging.info("Table name is ", table_name, " and the schema is ", schema_name)
        pandas_df.head(0).to_sql(
            name=table_name,
            schema=schema_name,
            con=db_engine, if_exists='replace', index=False)
        with tempfile.NamedTemporaryFile() as tmpfile:
            file_dir = os.path.dirname(os.path.realpath(tmpfile.name)) + '/temp_df.csv'
            pandas_df.to_csv(file_dir, index=False)
            cur = conn.cursor()
            f = open(file_dir, 'r')
            logging.info("File directory is {}{}".format(tmpfile, '/temp_df.csv'))
            cur.execute("Truncate {} Cascade;".format(full_table_name))
            logging.info("Truncated {}".format(full_table_name))
            cur.copy_expert("Copy {} from STDIN CSV HEADER QUOTE '\"'".format(full_table_name), f)
            cur.execute("commit;")
            logging.info("Loaded data into {}".format(full_table_name))