from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Depends
)
import csv
import time
import spacy
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from src.config import get_settings
from functools import cache
from src.text_model import AnalysisModel
from datetime import datetime

# Colocamos en una lista los datos de cada request de /analysis
execution_logs = []

_SETTINGS = get_settings()

app = FastAPI(
    title=_SETTINGS.service_name,
    version=_SETTINGS.k_revision
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Reemplaza con la URL de tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
text_model = AnalysisModel()

@app.get("/status")
def root():
    return {
        "status": "OK",
        "message": "API is running",
        "model": "openai - gpt_4 ",
        "service": "Análisis de textos jurídicos utilizando OpenAI",
        "version": "1.0.0",
        "author": "Camila Grandy Camacho y Ariane Garrett Becerra",
    }

@app.post("/analysis")
def analyze_text(text: str):
    start_time = datetime.now()

    # Llama al modelo de análisis
    doc = text_model.perform_analysis(text)

    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    log = {
        "endpoint": "/analysis",
        "date": str(time.ctime()),
        "text": text,
        "analysis": doc,
        "execution_time": execution_time,
    }

    execution_logs.append(log)

    return doc

@app.get("/reports")
def generate_report():
    if not execution_logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Por el momento no existen reportes!"
        )

    csv_file_path = "analysis_report.csv"

    with open(csv_file_path, mode="w", newline="") as csv_file:
        fieldnames = execution_logs[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(execution_logs)

    return FileResponse(csv_file_path, filename="analysis_report.csv", media_type="text/csv")