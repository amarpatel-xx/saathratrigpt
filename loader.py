import os

from langchain.document_loaders import CSVLoader
from astradb_session import initialize_astradb


# Function to load config and initialize AstraDB
def load_and_insert_data(csv_file_path):
    # Load configurations
    config = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ASTRA_DB_APPLICATION_TOKEN': os.getenv('ASTRA_DB_APPLICATION_TOKEN_VECTOR'),
        'ASTRA_DB_API_ENDPOINT': os.getenv('ASTRA_DB_API_ENDPOINT'),
        'ASTRA_DB_COLLECTION': os.getenv('ASTRA_DB_COLLECTION')
    }

    vstore = initialize_astradb(config)

    loader = CSVLoader(csv_file_path, metadata_columns=["Site", "Hotel", "Hotel_ID", "Date"])
    vstore.add_documents(documents=loader.load())
    print("Inserted clients into Astra DB")


# Call the function with paths
load_and_insert_data('resources/chatbot-faqs-tl.csv')
load_and_insert_data('resources/chatbot-faqs-qi.csv')
