from langchain.tools import BaseTool

from astradb_session import initialize_astradb

import os

# Determine the environment based on an environment variable
app_env = os.getenv('APP_ENV', 'dev')

if app_env == 'prod':
    from config_prod import *
else:
    from config_dev import *

# Load configurations
config = {
    'OPENAI_API_KEY': OPENAI_API_KEY,
    'ASTRA_DB_APPLICATION_TOKEN': ASTRA_DB_APPLICATION_TOKEN,
    'ASTRA_DB_API_ENDPOINT': ASTRA_DB_API_ENDPOINT,
    'ASTRA_DB_COLLECTION': ASTRA_DB_COLLECTION
}

# Initialize AstraDB
vstore = initialize_astradb(config)

### Client Similarity Tool Astra #########
class ClientSimilarityTool(BaseTool):
    name = "Hotel Frequently Asked Questions Tool"
    description = "This tool is used to answer questions frequently asked by our hotel's guests about our hotel, it's rooms and the services we provide." \
                  "Example query: what do you serve for breakfast?"

    def _run(self, user_question):
        print(f"The question from the user: {user_question}")
        client_list = vstore.similarity_search(user_question, k=3)

        for item in client_list:
            print(f"Found similar item: {item}.")

        return client_list

    def _arun(self, query: str):
        raise NotImplementedError("This tool does not support async")



