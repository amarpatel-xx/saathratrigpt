import os

from langchain.document_loaders import CSVLoader
from astradb_session import initialize_astradb

import os

# Determine the environment based on an environment variable
app_env = os.getenv('APP_ENV', 'dev')

if app_env == 'prod':
    from config_prod import *
else:
    from config_dev import *

# Function to load config and initialize AstraDB
def load_and_insert_data(csv_file_path):
    # Load configurations
    config = {
        'OPENAI_API_KEY': OPENAI_API_KEY,
        'ASTRA_DB_APPLICATION_TOKEN': ASTRA_DB_APPLICATION_TOKEN,
        'ASTRA_DB_API_ENDPOINT': ASTRA_DB_API_ENDPOINT,
        'ASTRA_DB_COLLECTION': ASTRA_DB_COLLECTION
    }

    vstore = initialize_astradb(config)

    loader = CSVLoader(csv_file_path, metadata_columns=["Site", "Hotel", "Hotel_ID", "Date"])
    vstore.add_documents(documents=loader.load())
    print("Inserted clients into Astra DB")


# Call the function with paths
load_and_insert_data(SAATHRATRI_GPT_DATA_LOAD_CSV_1)
load_and_insert_data(SAATHRATRI_GPT_DATA_LOAD_CSV_2)
