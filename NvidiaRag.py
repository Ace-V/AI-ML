import streamlit as st
import os
from langchain_nvidia_ai_endpoints import NVIDIAEmbeddings, ChatNVIDIA
from langchain_community.document_loaders import WebBaseLoader
from langchain.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
import time

from dotenv import load_dotenv
load_dotenv()

# Load the NVIDIA API key
os.environ['NVIDIA_API_KEY'] = os.getenv("NVIDIA_API_KEY")

def vector_embedding():
    """Create vector embeddings from PDF documents"""
    if "vectors" not in st.session_state:
        try:
            # Initialize embeddings
            st.session_state.embeddings = NVIDIAEmbeddings()
            
            # Check if directory exists
            pdf_directory = "./TEST"
            if not os.path.exists(pdf_directory):
                st.error(f"Directory '{pdf_directory}' does not exist. Please create it and add PDF files.")
                return False
            
            # Check if directory has PDF files
            pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
            if not pdf_files:
                st.error(f"No PDF files found in '{pdf_directory}' directory.")
                return False
            
            st.info(f"Found {len(pdf_files)} PDF files: {', '.join(pdf_files)}")
            
            # Data Ingestion
            st.session_state.loader = PyPDFDirectoryLoader(pdf_directory)
            st.session_state.docs = st.session_state.loader.load()
            
            if not st.session_state.docs:
                st.error("No documents were loaded. Please check your PDF files - they might be corrupted, password-protected, or contain only images.")
                return False
            
            st.info(f"Loaded {len(st.session_state.docs)} document pages")
            
            # Debug: Check if documents have content
            total_content_length = sum(len(doc.page_content.strip()) for doc in st.session_state.docs)
            if total_content_length == 0:
                st.error("All documents appear to be empty or contain no extractable text.")
                return False
            
            st.info(f"Total content length: {total_content_length} characters")
            
            # Chunk Creation
            st.session_state.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=700, 
                chunk_overlap=50
            )
            
            # Splitting - limit to first 30 documents or all if less than 30
            docs_to_process = st.session_state.docs[:30] if len(st.session_state.docs) > 30 else st.session_state.docs
            st.session_state.final_documents = st.session_state.text_splitter.split_documents(docs_to_process)
            
            if not st.session_state.final_documents:
                st.error("No text chunks were created from the documents. The documents might be too short or contain no readable text.")
                return False
            
            # Debug: Show chunk information
            st.info(f"Created {len(st.session_state.final_documents)} text chunks")
            
            # Filter out empty chunks
            st.session_state.final_documents = [doc for doc in st.session_state.final_documents if doc.page_content.strip()]
            
            if not st.session_state.final_documents:
                st.error("All text chunks are empty after filtering. Please check your PDF content.")
                return False
            
            st.info(f"After filtering empty chunks: {len(st.session_state.final_documents)} chunks remain")
            
            # Show sample of first chunk for debugging
            if st.session_state.final_documents:
                sample_text = st.session_state.final_documents[0].page_content[:200] + "..." if len(st.session_state.final_documents[0].page_content) > 200 else st.session_state.final_documents[0].page_content
                st.info(f"Sample text from first chunk: {sample_text}")
            
            # Create vector store
            st.session_state.vectors = FAISS.from_documents(
                st.session_state.final_documents, 
                st.session_state.embeddings
            )
            
            st.success(f"Successfully processed {len(st.session_state.final_documents)} text chunks from {len(docs_to_process)} documents.")
            return True
            
        except Exception as e:
            st.error(f"Error during vector embedding: {str(e)}")
            # Additional debugging information
            if hasattr(st.session_state, 'final_documents'):
                st.error(f"Number of final documents: {len(st.session_state.final_documents)}")
                if st.session_state.final_documents:
                    st.error(f"First document content length: {len(st.session_state.final_documents[0].page_content)}")
            return False
    
    return True

# Streamlit UI
st.title("NVIDIA NIM Demo")

# Check if API key is available
if not os.getenv("NVIDIA_API_KEY"):
    st.error("NVIDIA_API_KEY not found in environment variables. Please check your .env file.")
    st.stop()

# Initialize the LLM
try:
    llm = ChatNVIDIA(model="meta/llama3-70b-instruct")
except Exception as e:
    st.error(f"Error initializing NVIDIA LLM: {str(e)}")
    st.stop()

# Create prompt template
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the question.
    
    <context>
    {context}
    </context>
    
    Question: {input}
    
    Answer:
    """
)

# User input
prompt1 = st.text_input("Enter Your Question From Documents")

# Document embedding button
if st.button("Documents Embedding"):
    with st.spinner("Processing documents..."):
        if vector_embedding():
            st.success("Vector Store DB Is Ready")

# Question answering
if prompt1:
    # Check if vectors are available
    if "vectors" not in st.session_state:
        st.warning("Please click 'Documents Embedding' first to process your documents.")
    else:
        try:
            with st.spinner("Searching for answer..."):
                # Create document chain
                document_chain = create_stuff_documents_chain(llm, prompt)
                
                # Create retriever
                retriever = st.session_state.vectors.as_retriever()
                
                # Create retrieval chain
                retrieval_chain = create_retrieval_chain(retriever, document_chain)
                
                # Get response
                start = time.process_time()
                response = retrieval_chain.invoke({'input': prompt1})
                response_time = time.process_time() - start
                
                # Display results
                st.subheader("Answer:")
                st.write(response['answer'])
                
                st.info(f"Response time: {response_time:.2f} seconds")
                
                # Document similarity search results
                with st.expander("Document Similarity Search"):
                    if 'context' in response and response['context']:
                        for i, doc in enumerate(response["context"]):
                            st.write(f"**Document {i+1}:**")
                            st.write(doc.page_content)
                            st.write("---")
                    else:
                        st.write("No relevant documents found.")
                        
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")

# Sidebar with information
st.sidebar.header("Information")
st.sidebar.info(
    """
    This app uses NVIDIA's AI endpoints to answer questions based on your PDF documents.
    
    Steps:
    1. Make sure you have PDF files in the './TEST' directory
    2. Click 'Documents Embedding' to process documents
    3. Ask questions about your documents
    """
)

# Display session state info for debugging (optional)
if st.sidebar.checkbox("Show Debug Info"):
    st.sidebar.subheader("Session State")
    if "vectors" in st.session_state:
        st.sidebar.success("✅ Vector store created")
    else:
        st.sidebar.warning("❌ Vector store not created")
    
    if "docs" in st.session_state:
        st.sidebar.write(f"Documents loaded: {len(st.session_state.docs)}")
    
    if "final_documents" in st.session_state:
        st.sidebar.write(f"Text chunks: {len(st.session_state.final_documents)}")

#loda