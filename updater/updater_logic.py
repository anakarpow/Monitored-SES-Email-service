import pandas as pd
from updater.api_utils import query_and_return_dict
import utils
import json

# test data for local
file = 'test_data/Output (9).json'
with open(file, 'r') as foo:
    data = json.load(foo)

# query API 
# data=query_and_return_dict()

# unpack dict, return df with output info
output_df = utils.extract_contact_and_account_data(data)

test_json = output_df.to_dict(orient='records')
with open('test_data/draft_result.json', 'w') as file:
    json.dump(test_json, file)

# once data workflow is done
# if output_df is not empty
    # invoke lambda sending payload

