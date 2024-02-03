from syslog import LOG_PERROR
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
from langchain_core.messages import SystemMessage

from tools import ClientSimilarityTool
from astradb_session import initialize_memory, initialize_astradb

import os

# Load configurations
config = {
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'ASTRA_DB_APPLICATION_TOKEN': os.getenv('ASTRA_DB_APPLICATION_TOKEN_VECTOR'),
    'ASTRA_DB_API_ENDPOINT': os.getenv('ASTRA_DB_API_ENDPOINT'),
    'ASTRA_DB_COLLECTION': os.getenv('ASTRA_DB_COLLECTION')
}

# Initialize AstraDB
vstore = initialize_astradb(config)

# Initialize Tools
tools = [ClientSimilarityTool()]

# Initialize Memory
message_history = initialize_memory()

# Initialize Chat Model
llm = ChatOpenAI(openai_api_key=config['OPENAI_API_KEY'], temperature=0)

# Initialize System Message
system_message = SystemMessage(content="You are a hotel assistant for Travelodge by Wyndham Florida City / Homestead / Everglades. You help customers to answer frequently asked questions about our hotel and the services we offer.  If you do not know the answer, you prompt the guest to call 305-248-9777 or email frontdesk@travelodgefloridacity.com.  You are always polite, respectful, and sincere.")

# Initialize Agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
    memory=message_history,
    agent_kwargs={
        "system_message": system_message.content
    }
)

# Streamlit UI
st.title("Hotel Chatbot, the place to ask your questions about our hotel")
st.header("Welcome dear guest!")
user_question = st.text_input('Ask a question here:')

if len(user_question) > 5:
    try:
        with st.spinner(text="In progress..."):
            # Directly pass user_question as the argument to agent.run
            response = agent.run(input=user_question)
            st.write(response)
    except ValueError as ve:
        if "Could not parse LLM output" in str(ve):
            # Handle specific parsing error
            st.write("I'm sorry, but your message seems to be incomplete. Could you please provide more information or clarify your question?")
        else:
            st.error("An error occurred. Please try again.")
            st.write(str(ve))  # Display the error message
    except Exception as e:
        # Handle other exceptions
        st.error("An unexpected error occurred. Please try again.")
        st.write(str(e))  # Display the error message
