""" Web scraper for public data """

import pandas as pd
from sodapy import Socrata

# Below code snippet is from https://dev.socrata.com/foundry/data.cityofchicago.org/jaif-n74j

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("data.cms.gov", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(data.cms.gov,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("xbte-dn4t", limit=2000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)