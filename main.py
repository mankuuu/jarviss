from utils import invoke_chain
import streamlit as st
st.title("J.A.R.V.I.S.S. - Just A Really Very Intelligent School System 🤖✨")  


#Importing the environment variables and api-keys
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

from langchain_groq import ChatGroq


# Initialize Groq model
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = ChatGroq(
        model="llama3-groq-70b-8192-tool-use-preview",
        temperature=0,
        max_tokens=None,
        timeout=None,
    )

# initialize history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])




if prompt := st.chat_input("Ask me!"):
    # add latest message to history in format {role, content}
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.spinner("Generating response..."):
        with st.chat_message("assistant"):
            response = invoke_chain(prompt)
            print("Done\n\n")
            st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

