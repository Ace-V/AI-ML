import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate
import os 
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GROQ_API_KEY")
model=ChatGroq(model="gemma2-9b-It",api_key="api_key")
#Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"

##Prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant please respond to user queries."),
        ("user", "{question}"),
    ]
)

def generate_response(question,api_key,llm,temprature,max_tokens):

    api_key=api_key
    llm=model
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer=chain.invoke({"question": question})
    return answer

##Title
st.title("ChatBot using Groq API")
#api_key=st.text_input("Enter your Groq API Key", type="password")
#Temprature sidebar
temprature=st.sidebar.slider("Select the temprature",min_value=0.0,max_value=1.0,value=0.5)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

##Defining main interface
st.write("How can I help you today?")
user_input = st.text_input("Ask a question:")
if user_input:
    response=generate_response(user_input,api_key,model,temprature,max_tokens)
    st.write("Response:", response)
else:
    st.write("Please enter a question to get a response.")
