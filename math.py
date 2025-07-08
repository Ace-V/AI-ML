import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import llm_math,llm_symbolic_math,LLMChain,LLMMathChain
from langchain.chains import llm_checker
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool,initialize_agent
import os 
from dotenv import load_dotenv
load_dotenv()
from langchain.callbacks import StreamlitCallbackHandler

##Set streamlit
st.set_page_config(page_title="Text to math problem solver and search assistant")
st.title("Text to math solver Using GEMMA")

groq_api_key=st.sidebar.text_input(label="GROQ API KEY",type="password")

if not groq_api_key:
    st.info("Please add API key")
    st.stop()

llm=ChatGroq(model="gemma2-9b-it",api_key=groq_api_key,groq_api_key=groq_api_key)


##Initialize tools 
wiki=WikipediaAPIWrapper()
wiki_tool=Tool(
    name="wikipedia",
    func=wiki.run,
    description="a tool for searching the internet to solve your problem"
)

#Initialize math tools 
math_chain=LLMMathChain.from_llm(llm=llm)
calculator=Tool(
    name="calculator",
    func=math_chain.run,
    description="A tool for answering math related questions"
)

prompt="""
You are agent tasked to solve users mathematical question 
make sure the calculations you do are precise 
logically arrive at the solution 
and give a brief solution point wise
Question:{question}
Answer:
"""

prompt_template=PromptTemplate(
    input_variables=["question"],
    template=prompt
)

##Math problem tool 
chain=LLMChain(llm=llm,prompt=prompt_template)

reasoning_tool=Tool(
    name="Reasoning",
    func=chain.run,
    description="Tools to answer logical based and reasoning question"
)

#Initialize the agents 

assistant_agent=initialize_agent(
    tools=[wiki_tool,calculator,reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assisant","content":"Hi, Im a math chatbot who can answer all your maths and logical questions"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

#Handler function
#def generate_response(question):
#    response=assistant_agent.invoke({'input':question})
#    return response

#Interaction 
question=st.text_area("Enter your Question:","How many units are in a dozen")

if st.button("Find my answers"):
    if question:
        with st.spinner("Generate Response..."):
            st.session_state.messages.append({"role":"user","content":question})
            st.chat_message("user").write(question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])

            st.session_state.messages.append({'role':'assistant','content':response})
            st.write('###Response:')
            st.success(response)
    
    else:
        st.warning("please enter the question")



