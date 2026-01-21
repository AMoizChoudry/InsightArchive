from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.agent import chat_with_pdf
from core.rag_engine import ingest_pdf
import shutil
import os

app = FastAPI(title="PDF Chatter API")

# Define what a message looks like
class ChatRequest(BaseModel):
    message: str

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Receives a PDF, saves it temporarily, and indexes it."""
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # Index the file into LanceDB
        ingest_pdf(temp_path)
        return {"message": f"Successfully indexed {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # We MUST capture both values from the agent
        answer, metrics = chat_with_pdf(request.message) 
        # Return them as a dictionary so FastAPI can JSON-serialize them
        return {"response": answer, "metrics": metrics}
    except Exception as e:
        # This is what's catching the error and turning it into a 500
        print(f"CRITICAL ERROR: {e}") 
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/clear")
async def clear_database():
    """Deletes the existing vector database to start fresh."""
    db_path = "./.lancedb"
    if os.path.exists(db_path):
        try:
            shutil.rmtree(db_path)
            return {"message": "Database cleared successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to delete: {str(e)}")
    return {"message": "Database already empty."}

if __name__ == "__main__":
    import uvicorn
    # Start the server on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000)