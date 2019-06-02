""" Transform for Studying the Pharmacy data from CMS """
import pandas as pd
import numpy as np
import abc
import attr


@attr.s(frozen=True)
class BaseProvider(object):
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