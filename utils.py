import os
from dotenv import load_dotenv
load_dotenv()


#Loading the database
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")


#Loading the api-keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")


from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_groq import ChatGroq
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.chat_message_histories import ChatMessageHistory

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough
from prompts import final_prompt, answer_prompt


#Loading the suffix
from additionals import suffix
import streamlit as st

#Creating the chain
# @st.cache_resource
def get_chain(question):
    print("Creating chain")
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")   
    print("Connected Database") 

    #Initiating the LLM
    llm = ChatGroq(
    model="llama3-groq-70b-8192-tool-use-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    )
    print("llm initiated")

    #1st phase
    generate_query = create_sql_query_chain(llm, db,final_prompt) 
    query = generate_query.invoke({"question": question})
    print(query)
    print("generate_query")

    #2nd phase
    execute_query = QuerySQLDataBaseTool(db=db)
    print("execute_query")

    #3rd phase
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    print("rephrase_answer")


    # chain = generate_query | execute_query
    #Final phase
    chain = (
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
    )
    print("chain created")

    return chain


#Adding History, commenting for now. Have to implement some clear memory functionalities for better working
# def create_history(messages):
#     history = ChatMessageHistory()
#     for message in messages:
#         if message["role"] == "user":
#             history.add_user_message(message["content"])
#         else:
#             history.add_ai_message(message["content"])
#     return history

#This is the function to be called from main.py which encapsulates all other functions.
#As history is commented , will be commenting many function calls inside and providing alternate options
def invoke_chain(question):
    chain = get_chain(question)
    # history = create_history(messages)
    print("going to call chain.invoke")
    response = chain.invoke({"question": question})
    print("after chain.invoke")
    # response = chain.invoke({"question": question + suffix ,"top_k":3})
    # history.add_user_message(question)
    # history.add_ai_message(response)
    return response