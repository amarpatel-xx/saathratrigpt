import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ASTRA_DB_APPLICATION_TOKEN = os.getenv('ASTRA_DB_APPLICATION_TOKEN_VECTOR')
ASTRA_DB_API_ENDPOINT = os.getenv('ASTRA_DB_API_ENDPOINT')
ASTRA_DB_COLLECTION = os.getenv('ASTRA_DB_COLLECTION_PROD')
SAATHRATRI_GPT_DATA_LOAD_CSV_1 = os.getenv('SAATHRATRI_GPT_DATA_LOAD_CSV_1')
SAATHRATRI_GPT_DATA_LOAD_CSV_2 = os.getenv('SAATHRATRI_GPT_DATA_LOAD_CSV_2')
SAATHRATRI_ORCHESTRATOR_GATEWAY_API_URL = os.getenv('SAATHRATRI_ORCHESTRATOR_GATEWAY_API_URL')