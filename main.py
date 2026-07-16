from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

# Humare specific module imports
from agents.orchestrator import FinSightOrchestrator
from tools.name_resolver import resolve_ticker

app = FastAPI()

# CORS configuration taaki React frontend se access block na ho
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema for input validation
class AnalysisRequest(BaseModel):
    company: str
    headlines: list[str]

# Helper function jo NumPy types ko standard Python types mein badalta hai
# Isse FastAPI JSON response generate karte waqt crash nahi karega
def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(v) for v in obj]
    elif isinstance(obj, (np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    return obj

@app.post("/analyze")
def analyze(req: AnalysisRequest):
    try:
        # Step 1: Company name se ticker resolve karo, fallback to uppercase string
        ticker = resolve_ticker(req.company) or req.company.upper()
        
        # Step 2: Orchestrator instance banao aur ticker pass karo
        orchestrator = FinSightOrchestrator(ticker)
        
        # Step 3: Headlines pass karke run method call karo
        report = orchestrator.run(req.headlines)
        
        # Step 4: Data cleaner function call karke return karo
        return convert_numpy(report)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))