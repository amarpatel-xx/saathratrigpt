from syslog import LOG_PERROR
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
import streamlit as st
from langchain_core.messages import SystemMessage

from tools import ClientSimilarityTool
from astradb_session import initialize_memory, initialize_astradb

import os

import numpy as np

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

prompt_message = "Ask me anything about our hotel, the local area, or your stay?"
welcome_message = "Hello 👋 Friend! " + prompt_message

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Accept user input
    with st.chat_message("assistant"):
        st.write(welcome_message)
        st.session_state.messages.append({"role": "assistant", "content": welcome_message})
else:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input

if prompt := st.chat_input(prompt_message):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            # Directly pass user_question as the argument to agent.run
            response = agent.run(input=prompt)

            # Embed the JavaScript code in the Streamlit app
            st.write(response)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})