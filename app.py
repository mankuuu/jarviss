from utils import invoke_chain
import streamlit as st

#Importing the environment variables and api-keys
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# internet = os.getenv("INTERNET", "False").lower() == "true"

from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama

# if internet :
# llm = ChatGroq(
#         model="llama3-groq-70b-8192-tool-use-preview",
#         temperature=0,
#         max_tokens=None,
#         timeout=None,
#     )
# else :

#     llm = ChatOllama(model="llama3.1" , temperature= 0)

# Initialize Groq model
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = ChatGroq(
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
    )

# # Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    print("First Time")
else :
    print(type(st.session_state.messages))
    print(st.session_state.messages)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ask me?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    print(st.session_state.messages)
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.spinner("Thinking..."):
        with st.chat_message("assistant"):
            try:
                response = invoke_chain(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


#########################################
# Input for prompt
# prompt = st.chat_input("Hello, Ask me!")

# if prompt :

#     #Display input prompt
#     with st.chat_message("user"):
#         st.write(prompt)

#     #Processing
#     with st.spinner("Thinking...."):
#         response = invoke_chain(prompt)
#         st.markdown(response)