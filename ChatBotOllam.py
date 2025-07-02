from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import Ollama
import streamlit as st
import os 
from dotenv import load_dotenv
load_dotenv()
#Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"

#Prompt template
prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant please respond to user queries."),
        ("user", "Question:{question}"),
    ]
)

def generate_response(question, model, temperature,max_tokens):
    llm = Ollama(model="gemma3",temperature=temperature, num_predict=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({"question": question})
    return answer
##Title
st.title("ChatBot using Ollama")
#api_key=st.text_input("Enter your Groq API Key", type="password")
#Temprature sidebar
temprature=st.sidebar.slider("Select the temprature",min_value=0.0,max_value=1.0,value=0.5)
max_tokens=st.sidebar.slider("Max Tokens",min_value=50,max_value=300,value=150)

##Defining main interface
st.write("How can I help you today?")
user_input = st.text_input("Ask a question:")
if user_input:
    response=generate_response(user_input,"gemma3",temprature,max_tokens)
    st.write("Response:", response)
else:
    st.write("Please enter a question to get a response.")
