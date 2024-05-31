README
# RAG Chat with Your PDF
## This project is a FastAPI-based application that allows users to upload PDF documents and interact with them via a chat interface. The backend processes the documents, extracts relevant information, and enables natural language querying. <br />

![alt text](https://github.com/danielelongo14/rag-chat-with-your-pdf/blob/947365e4cf558719efa0fb7fd436fbfccc4c7609/Rag.png)


## Features <br />

Document Upload: Upload PDF documents. <br />
Document Parsing: Extract content from PDFs using LlamaParse. <br />
Embeddings and Vector Store: Generate embeddings for document content and store them in Weaviate. <br />
Chat Interface: Query the documents using natural language. <br />
Prerequisites <br />
Python 3.8 or higher <br />
Node.js <br />
Docker (optional, for containerized deployment) <br />



## Environment Variables <br />

Set the following environment variables in your .env file: <br />
GROK_RAGAPP: API key for Groq Chat. <br />
LLAMA_CLOUD_KEY: API key for LlamaParse. <br />
DATA_FOLDER: Directory to store uploaded documents. <br />
WEAVIATE_CLUSTER_URL: Weaviate instance URL. <br />
WEAVIATE_API_KEY: Weaviate API key. <br />


## Setup <br />

Clone the Repository <br />
git clone https://github.com/danielelongo14/rag-chat-with-your-pdf.git <br />
cd rag-chat-with-your-pdf<br />
docker-compose up --build<br />



## Key Components <br />

FastAPI: Backend framework for handling requests.<br />
LlamaParse: Library for parsing PDF documents. <br />
Weaviate: Vector database for storing and retrieving embeddings.<br />
React: Frontend framework for the chat interface.<br />



## Repository Structure <br />

rag-chat-with-your-pdf/ <br />
├── frontend/          # Frontend React application<br />
├── ragApp/            # Backend FastAPI application <br />
├── .gitignore         # Git ignore file<br />
├── docker-compose.yml # Docker Compose configuration<br />
