""" Transform for Studying the Pharmacy data from CMS """
import pandas as pd
import numpy as np
import abc
import attr
import sqlalchemy as sa
import psycopg2


def get_pharm_data(db_url, table_name, schema_name):
    """
    Crawl data from given postgres db_url
    :param db_url: postgresql database address
    :return: pandas dataframe
    """
    with psycopg2.connect(database=db_url) as conn:
        conn.execute










@attr.s(frozen=True)
class BaseProvider(abc.ABC):
    """ Base Provider class """

    first_name = attr.ib()
    last_name = attr.ib()
    npi = attr.ib()
    city = attr.ib()
    specialty = attr.ib()
    drug_list = attr.ib(factory=list)

    def add_to_drug_list(self, new_drug_list):
        for drug in new_drug_list:
            self.drug_list.append(drug)