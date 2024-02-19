# hotel-chatbot
Bankflix is a chatbot using LangChain and AstraDB


This assistant is built on [RAGStack-AI](https://docs.datastax.com/en/ragstack/docs/quickstart.html) and [AstraPy](https://github.com/datastax/astrapy)

It is powered by OpenAI to build embeddings and Astra to store the data.

## Pre-requisites

- Python 3.6+
- Launch an [AstraDB](https://astra.datastax.com/) vector database

## Setup

- Clone the repository
- Install the dependencies using `pip3 install -r requirements.txt`

## Development Data Load
- Run the loader `APP_ENV=dev python3 loader.py`
## Production Data Load
- Run the loader `APP_ENV=prod python3 loader.py`

## Running the Application Locally
- Run `APP_ENV=dev loader.py` to import fake clients data in your Astra db collection from `resources/clients-dataset.csv`
- Run `main.py` using the command `APP_ENV=dev streamlit run main.py`

