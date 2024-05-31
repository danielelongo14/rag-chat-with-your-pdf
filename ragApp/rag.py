import os
import textwrap
from pathlib import Path

from IPython.display import Markdown
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
#from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_groq import ChatGroq
from llama_parse import LlamaParse
import weaviate
import weaviate.classes as wvc
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.vectorstores import Weaviate


groqKey = os.getenv('GROK_RAGAPP')
llamaCloudKey = os.getenv('LLAMA_CLOUD_KEY')
dataFolder = os.getenv("DATA_FOLDER")

embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", api_key=groqKey)


prompt_template = """
Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Answer the question and provide additional helpful information,
based on the pieces of information, if applicable. Be succinct.

Responses should be properly formatted to be easily read.
"""

prompt = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
     


#WEAVIATE CLIENT
client = weaviate.Client(
    url=os.getenv("WEAVIATE_CLUSTER_URL"),  # Replace with your Weaviate Cloud URL
    auth_client_secret=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),  # Replace with your Weaviate Cloud key
)

# Define a class schema
class_obj = {
    "class": "Document",
    "description": "A class representing a document with embeddings",
    "properties": [
        {
            "name": "title",
            "dataType": ["text"],
            "description": "Title of the document"
        },
        {
            "name": "content",
            "dataType": ["text"],
            "description": "Content of the document"
        },
        {
            "name": "embedding",
            "dataType": ["blob"],
            "description": "Embedding vector of the document"
        }
    ]
}

# Add the class to Weaviate

def print_response(response):
    response_txt = response["result"]
    for chunk in response_txt.split("\n"):
        if not chunk:
            print()
            continue
        print("\n".join(textwrap.wrap(chunk, 100, break_long_words=False)))



async def parse_document(document_path):
    instruction = """The provided document is a Machine Learning and AI research paper.
This form provides detailed information about the research, including the abstract, introduction, related work, methodology, experiments, results, discussions, and conclusions.
It includes various sections with technical details, equations, diagrams, and tables.
Ensure to capture key elements like the research objective, proposed methods, datasets used, evaluation metrics, and significant findings.
Try to be precise and thorough while extracting the information."""

    document_path_name = document_path.split("/")[-1].split(".")[0]

    parser = LlamaParse(
    api_key=llamaCloudKey,
    result_type="markdown",
    parsing_instruction=instruction,
    max_timeout=5000,
)
    #llama_parse_documents = parser.load_data(document_path)

    llama_parse_documents =  await parser.aload_data(document_path)
    

    #print(llama_parse_documents)
    parsed_doc = llama_parse_documents[0]
    print("Parsed doc: ", parsed_doc.text)
    
    document_path = Path(f"data/{document_path_name}.md")
    with document_path.open("a") as f:
        f.write(parsed_doc.text)
    
    #Implement without saving the file to disk TBD
    md_document_name = (f"{document_path_name}.md")
    return md_document_name

def split_doc(md_document_name):
    # Load the document
    document_loader = UnstructuredMarkdownLoader(f"./data/{md_document_name}")
    document = document_loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap=128)
    docs = text_splitter.split_documents(document)

    return docs

def upload_embeddings(docs, embeddings, client):

    vector_db = Weaviate.from_documents(
    docs, embeddings, client=client, by_text=False
    )

    return vector_db

def retrieve_documents(vector_db,query ):

    retriever = vector_db.as_retriever(k=3)
    compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2")
    compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=retriever
    )
    
    qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=compression_retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt, "verbose": True},
    )

    response = qa.invoke(query)

    return response 


def main():
    
    document_parsed = parse_document("./data/test2.pdf")
    #print(document_parsed)
    
    splitted_docs = split_doc(document_parsed)
    #print(properties)
    
    vector_db = upload_embeddings(splitted_docs, embeddings, client)
    #print(uploaded)
    query = "What is the most significant innovation from the paper?"
    response = retrieve_documents(vector_db, query)
    #print(response)
    print(Markdown(response["result"]))




