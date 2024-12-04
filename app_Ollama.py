from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st 
import os
from dotenv import load_dotenv
load_dotenv()

## Langsmith Tracking :
os.environ['LANGCHAIN_API_KEY']="Enter LangChain key here"
os.environ['LANGCHAIN_TRACING_V2']="true"
os.environ['LANCHIAN_PROJECT']="Q&A Chatbot With Ollama"

## Prompt template:

prompt=ChatPromptTemplate.from_messages(
    [
        ("system" , "Your are a helpful assistant . Please response to the user queries"),
        ("user" , "Question:{question}")
    ]
)

def generate_response(question , engine , temp , max_token):
    llm=Ollama(model=engine)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    ans=chain.invoke({'question':question})
    return ans

st.title("Q&A Chatbot using Ollama")

#sidebar for settings
st.sidebar.title("Settings")

## Drop Down to select model
engine=st.sidebar.selectbox("Select the Model" , ["gemma:2b"  , "gemma2:2b"])

#Adjust the response:
temprature=st.sidebar.slider("Temprature" , min_value=0.0 , max_value=1.0 , value=0.7)
max_tokens=st.sidebar.slider("Max Token" , min_value=50 , max_value=300 , value=150)

## Main interface:
st.write("Ask the question")
user_input=st.text_input("You : ")

if user_input:
    response=generate_response(user_input  , engine ,temprature , max_tokens)
    st.write(response)
else:
    st.write("Please provide the query")
