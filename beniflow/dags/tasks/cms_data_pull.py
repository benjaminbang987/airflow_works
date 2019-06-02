""" Web scraper for CMS Pharmacy data """

import pandas as pd
from sodapy import Socrata
from beniflow_utils import utils

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





def run_cms_data_pull(website_link, dataset_identifier, crawl_limit, db_url, db_url_full,
                      schema, table_name, token=None):
    """
    Function that pulls the CMS data
    """
    results_df = crawl_website_socrata(website_link=website_link,
                                       token=token,
                                       dataset_identifier=dataset_identifier,
                                       crawl_limit=crawl_limit)
    utils.pd_to_sql_wrapper(table_name,
                            schema,
                            results_df,
                            db_url,
                            db_url_full)
