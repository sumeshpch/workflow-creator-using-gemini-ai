from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from gemini_model import GeminiModel, LanguageSelection
import json
from datetime import datetime
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)

# Initialize the model
model = GeminiModel(
    api_key="AIzaSyB9-0000000000000000000000000000000",
    selected_language=LanguageSelection.ENGLISH
)

class WorkflowRequest(BaseModel):
    message: str
    language: Optional[str] = "english"
    history: Optional[list] = None

class WorkflowResponse(BaseModel):
    workflow: Dict[str, Any]
    timestamp: str

def load_history() -> List[dict]:
    if os.path.exists('history.json'):
        with open('history.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history: List[dict]):
    with open('history.json', 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

@app.post("/workflow", response_model=WorkflowResponse)
async def workflow(request: WorkflowRequest):
    try:
        # Convert language string to LanguageSelection enum
        language_map = {
            "english": LanguageSelection.ENGLISH,
            "malayalam": LanguageSelection.MALAYALAM,
            "hindi": LanguageSelection.HINDI,
            "arabic": LanguageSelection.ARABIC
        }
        
        selected_language = language_map.get(request.language.lower(), LanguageSelection.ENGLISH)
        
        # Update model language if different
        if model.selected_language != selected_language:
            model.selected_language = selected_language
        
        # Start workflow generation with history if provided
        if request.history:
            model.start_chat(history=request.history)
        
        # Get response from model
        response = model.send_message(request.message)
        
        # Create response object
        workflow_response = WorkflowResponse(
            workflow=response,
            timestamp=datetime.now().isoformat()
        )
        
        # Load existing history
        # history = load_history()
        
        # Add new chat entry
        # history.append({
        #     "timestamp": workflow_response.timestamp,
        #     "request": {
        #         "message": request.message,
        #         "language": request.language
        #     },
        #     "response": workflow_response.workflow
        # })
        
        # Save updated history
        # save_history(history)
        
        return workflow_response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history():
    try:
        return load_chat_history()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Gemini Chat API is running"}

@app.get("/workflow")
async def read_workflow():
    return {"message": "Workflow endpoint. Please use POST method to generate workflow with payload {message: <message>, language: <language>, history: <history>}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 