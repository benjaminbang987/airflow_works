""" Web scraper for CMS Pharmacy data """

import pandas as pd
from sodapy import Socrata
from sqlalchemy import create_engine
import psycopg2
import logging
import tempfile
import os


def crawl_website_socrata(website_link, dataset_identifier, crawl_limit, token=None):
    """
    Simple crawler for a specific file
    Code snippet is from https://dev.socrata.com/foundry/data.cityofchicago.org/jaif-n74j
    """
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata(website_link, token)
    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cms.gov,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get(dataset_identifier, limit=crawl_limit)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    return results_df


def pd_to_sql_wrapper(table_name, schema, pandas_df, db_url, db_url_full):
    """
    Wrapper function to speed up pandas.to_sql function
    """
    full_table_name = schema + "." + table_name
    db_engine = create_engine(db_url_full)
    with psycopg2.connect(database=db_url) as conn:
        logging.info("Table name is ", table_name, " and the schema is ", schema)
        logging.info(db_url)
        logging.info(conn)
        pandas_df.head(0).to_sql(
            name=table_name,
            schema=schema,
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



def run_cms_data_pull(website_link, dataset_identifier, crawl_limit, db_url, db_url_full,
                      schema, table_name, token=None):
    """
    Function that pulls the CMS data
    """
    results_df = crawl_website_socrata(website_link=website_link,
                                       token=token,
                                       dataset_identifier=dataset_identifier,
                                       crawl_limit=crawl_limit)
    pd_to_sql_wrapper(table_name,
                      schema,
                      results_df,
                      db_url,
                      db_url_full)
