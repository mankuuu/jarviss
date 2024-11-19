from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from additionals import suffix

example_prompt = ChatPromptTemplate.from_messages(              #The above examples will be presented to llm in this format
    [
        # ("human" , "{input}\nSQLQuery:"),
        ("human" , "{input}. " + suffix),
        ("ai" , "{query}"), 
    ]
)


few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=get_example_selector(),
    input_variables=["input","top_k"],
)


# final_prompt = ChatPromptTemplate.from_messages(
#      [
#          ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for reference and may be considered while answering follow up questions"),
#          few_shot_prompt,
#          MessagesPlaceholder(variable_name="messages"),             #adding the past conversation if happened.
#          ("human", "{input}"),
#      ]
#  )

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)


answer_prompt = PromptTemplate.from_template(
     """Given the following user question, corresponding SQL query, and SQL result, answer the user question in natural english language.If the result is blank, then answer in negative.

 Question: {question}
 SQL Query: {query}
 SQL Result: {result}
 Answer: """
 )