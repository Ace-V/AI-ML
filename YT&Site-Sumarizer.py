import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader
import os
from dotenv import load_dotenv
load_dotenv()

#Streamlit app
st.set_page_config(page_title="Langchain--> Summarize Text from youtube or websites")
st.title("Site and Youtube Summarizer")
st.subheader("Summarize URL")

groq_api_key=os.getenv("GROQ_API_KEY")
llm=ChatGroq(model="gemma2-9b-it",api_key=groq_api_key)

prompt_template="""
HEY provide summary of the following content in 300 words:
content{text}

"""

prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

##Get Groq and url space for yt or site
with st.sidebar:
    groq_api_key=st.text_input("Groq api key",value="",type="password")   

generic_url=st.text_input("URL",label_visibility="collapsed")

if st.button("summarize the content"):
    ## Validate inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide correct information")
    elif not validators.url(generic_url):
        st.error("Please enter Valid URL")
    else:
        try:
            with st.spinner("Waiting..."):
                ##load the url 
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    # Clean YouTube URL - remove tracking parameters
                    if "youtu.be" in generic_url:
                        video_id = generic_url.split("/")[-1].split("?")[0]
                        clean_url = f"https://www.youtube.com/watch?v={video_id}"
                    else:
                        clean_url = generic_url.split("&")[0]  # Remove additional parameters
                    
                    try:
                        loader=YoutubeLoader.from_youtube_url(clean_url, add_video_info=False)
                    except Exception as yt_error:
                        st.error(f"YouTube loading failed: {yt_error}")
                        st.info("Try using the full YouTube URL format: https://www.youtube.com/watch?v=VIDEO_ID")
                        st.stop()
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"})
                
                # Load data (this works for both YouTube and regular URLs)
                data=loader.load()

                ##Initialize Chain for summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(data)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception{e}")
#streamlit run YT&LINK-Sumarize