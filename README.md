README
RAG Chat with Your PDF
This project is a FastAPI-based application that allows users to upload PDF documents and interact with them via a chat interface. The backend processes the documents, extracts relevant information, and enables natural language querying.

Features
Document Upload: Upload PDF documents.
Document Parsing: Extract content from PDFs using LlamaParse.
Embeddings and Vector Store: Generate embeddings for document content and store them in Weaviate.
Chat Interface: Query the documents using natural language.
Prerequisites
Python 3.8 or higher
Node.js
Docker (optional, for containerized deployment)
Environment Variables
Set the following environment variables in your .env file:

GROK_RAGAPP: API key for Groq Chat.
LLAMA_CLOUD_KEY: API key for LlamaParse.
DATA_FOLDER: Directory to store uploaded documents.
WEAVIATE_CLUSTER_URL: Weaviate instance URL.
WEAVIATE_API_KEY: Weaviate API key.
Setup

Clone the Repository
git clone https://github.com/danielelongo14/rag-chat-with-your-pdf.git
cd rag-chat-with-your-pdf
docker-compose up --build

Key Components
FastAPI: Backend framework for handling requests.
LlamaParse: Library for parsing PDF documents.
Weaviate: Vector database for storing and retrieving embeddings.
React: Frontend framework for the chat interface.
Repository Structure


rag-chat-with-your-pdf/
├── frontend/          # Frontend React application
├── ragApp/            # Backend FastAPI application
├── .gitignore         # Git ignore file
├── docker-compose.yml # Docker Compose configuration
