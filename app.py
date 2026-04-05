import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.database import ErrorDB
from src.llm import FixGenerator
from fastapi.responses import FileResponse

app = FastAPI(title="AI Bug Fix Bot")

# Lazy initialize
db = None
generator = None

# Request models
class IngestRequest(BaseModel):
    file_path: str

class SuggestRequest(BaseModel):
    error_log: str

@app.on_event("startup")
async def startup_event():
    global db, generator
    db = ErrorDB()
    try:
        generator = FixGenerator()
    except ValueError:
        print("Warning: GEMINI_API_KEY environment variable is missng.")

@app.post("/api/ingest")
async def ingest_data(req: IngestRequest):
    try:
        db.ingest_data(req.file_path)
        return {"status": "success", "message": f"Successfully ingested {req.file_path}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/suggest")
async def suggest_fix(req: SuggestRequest):
    if not generator:
        raise HTTPException(status_code=500, detail="LLM Generator not initialized. Ensure GEMINI_API_KEY is set.")
    
    try:
        similar_cases = db.query_similar_errors(req.error_log, n_results=2)
        suggestion = generator.generate_fix(req.error_log, similar_cases)
        return {"suggestion": suggestion}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

# Mount static directory for frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")
