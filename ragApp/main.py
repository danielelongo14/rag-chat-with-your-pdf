import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
from fastapi.middleware.cors import CORSMiddleware
from rag import (
    parse_document,
    split_doc,
    upload_embeddings,
    retrieve_documents,
    embeddings,
    client
)



dataFolder = os.getenv("DATA_FOLDER")
print("Data folder: ", dataFolder)
vector_db = None

app = FastAPI()


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],  # Adjust as needed
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    file_location = f"{dataFolder}/{file.filename}"
    print("File location: ", file_location)
    print(file_location)
    try:
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        document_parsed =await parse_document(file_location)
        splitted_docs = split_doc(document_parsed)
        global vector_db
        vector_db = upload_embeddings(splitted_docs, embeddings, client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

    return JSONResponse(content={"message": "Document uploaded and processed successfully."})

@app.post("/chat/")
async def chat_with_document(query: Query):
    try:
        #vector_db = Weaviate.as_retriever(client=client)
        response = retrieve_documents(vector_db, query.query)
        return JSONResponse(content={"response": response["result"]})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)