from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain_groq import ChatGroq
from datasets import load_dataset
import os 
from dotenv import load_dotenv
load_dotenv()
import cassio
from PyPDF2 import PdfReader
from typing_extensions import Concatenate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter , CharacterTextSplitter

ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_ID=os.getenv("ASTRA_DB_ID")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
HF_TOKEN=os.getenv("HF_TOKEN")
pdfreader=PdfReader("The_Stranger.pdf")


raw_text=''
for i , page in enumerate(pdfreader.pages):
    content=page.extract_text()
    if content:
        raw_text+= content

cassio.init(token=ASTRA_DB_APPLICATION_TOKEN,database_id=ASTRA_DB_ID)
llm=ChatGroq(model="llama-3.1-8b-instant",api_key=GROQ_API_KEY)
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")
embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


astra_vector_store = Cassandra(
    embedding=embeddings,
    table_name="qa_mini",
    session=None,
    keyspace=None,
)

text_splitter= CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)

texts=text_splitter.split_text(raw_text)

astra_vector_store.add_texts(texts)
astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)


first_question=True
while True:
    if first_question:
        query_text=input("\nEnter Your Question:").strip()
    else:
        query_text=input("Whats your next question?").strip()

    if query_text.lower()=="quit":
        break

    if query_text=='':
        continue

    first_question=False

    print("\nQuestion: \"%s\"" % query_text)
    answer=astra_vector_index.query(query_text,llm=llm).strip()
    print("Answer: \"%s\"\n" % answer)

    print("First Document By Relevance:::")
    for doc,score in astra_vector_store.similarity_search_with_score(query_text,k=4):
        print("   [%0.4f] \"%s...\""%(score,doc.page_content[:84]))