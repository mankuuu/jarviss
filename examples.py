examples = [                                #These examples behave like training set to llm making it to believe we had a conversation like this
    {
        "input" : "List all students of the class" , 
        "query" : "SELECT * FROM students;"
    } ,
    {
        "input" : "Give me the usn of all students" , 
        "query" : "SELECT student_id FROM students;"
    } ,
    {
        "input" : "Give me details of student id 106" , 
        "query" : "SELECT * FROM students WHERE student_id = '1DS21CS106'"
    } ,
    {
        "input" : "Who is 087?" , 
        "query" : "SELECT * FROM students WHERE student_id = '1DS21CS087'"
    } ,
    {
        "input" : "Give me details of student id 1ds21cs087" , 
        "query" : "SELECT * FROM students WHERE student_id = '1DS21CS087'"
    } ,
    {
        "input" : "Give me details of usn 234" , 
        "query" : "SELECT * FROM students WHERE student_id = '1DS21CS234'"
    } ,
    {
        "input" : "Give me details of usn 1ds21cs234" , 
        "query" : "SELECT * FROM students WHERE student_id = '1DS21CS234'"
    } , 
    {
        "input" : "Who teaches ar vr?" ,
        "query" : "SELECT teacher_name FROM teachers INNER JOIN teacher_subject ON teachers.teacher_id = teacher_subject.teacher_id INNER JOIN subjects ON teacher_subject.subject_id = subjects.subject_id WHERE subjects.subject_name = 'AR VR';"
    } , 
    {
        "input" : "Who teaches business intelligence?" ,
        "query" : "SELECT teacher_name FROM teachers INNER JOIN teacher_subject ON teachers.teacher_id = teacher_subject.teacher_id INNER JOIN subjects ON teacher_subject.subject_id = subjects.subject_id WHERE subjects.subject_name = 'Business Intelligence';"
    } ,
    {
        "input" : "What Premsukh teaches?" ,
        "query" : "select su.subject_name from teachers t inner join teacher_subject ts on t.teacher_id = ts.teacher_id inner join subjects su on su.subject_id = ts.subject_id where t.teacher_id in (select teacher_id from teachers where teacher_name like '%premsukh%'); "
    } ,
    {
        "input" : "what Harsh teaches?" , 
        "query" : "select su.subject_name from teachers t inner join teacher_subject ts on t.teacher_id = ts.teacher_id inner join subjects su on su.subject_id = ts.subject_id where t.teacher_id in (select teacher_id from teachers where teacher_name like '%harsh%'); "
    } ,
    {
        "input" : "How many subjects Tanmayi teaches?" ,
        "query" : "SELECT COUNT(*) FROM teacher_subject ts WHERE teacher_id IN (SELECT teacher_id FROM teachers t WHERE t.teacher_name LIKE '%tanmayi%');"
    } ,
]


#Dynamic few-shot selections
from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_ollama import OllamaEmbeddings
# import streamlit as st

# @st.cache_resource
def get_example_selector():
    print("Inside example selector")
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OllamaEmbeddings(model="llama3.1",),
        Chroma,
        k=2,
        input_keys=["input"],
    )
    print("exiting example_selector")
    return example_selector