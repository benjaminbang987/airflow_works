""" Web scraper for public data """

import pandas as pd
from sodapy import Socrata
import game_1 as g1
import psycopg2


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


def run_cms_data_pull(website_link, dataset_identifier, crawl_limit, db_url, schema, table_name, token=None):
    """
    funciton that pulls the CMS data
    """
    results_df = crawl_website_socrata(website_link=website_link,
                                       token=token,
                                       dataset_identifier=dataset_identifier,
                                       crawl_limit=crawl_limit)
    with psycopg2.connect(database=db_url) as conn:
        g1.psql_insert_copy(table_name=table_name,
                            table_schema=schema,
                            conn=conn,
                            keys=results_df.keys(),
                            data_iter=results_df.values)


""" 
example raw html web crawler - but not really necessary since I can use Socrata API for CMS website.
"""
# page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
# tree = html.fromstring(page.content)