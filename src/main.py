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
from src.text_model import AnalysisModel
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse

sqlite_file = "db.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Colocamos en una lista los datos de cada request de /analysis
execution_logs = []

_SETTINGS = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creamos la base de datos
    create_db_and_tables()
    yield

app = FastAPI(
    title=_SETTINGS.service_name,
    version=_SETTINGS.k_revision,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
def analyze_text(text: str, db: Session = Depends(get_session)):
    start_time = datetime.now()

    # Llama al modelo de análisis
    doc = text_model.perform_analysis(text)

    end_time = datetime.now()
    execution_time = (end_time - start_time).total_seconds()

    # Añadimos el log para obtener luego un reporte
    log = {
        "endpoint": "/analysis",
        "date": str(time.ctime()),
        "text": text,
        "analysis": doc,
        "execution_time": execution_time,
    }
    execution_logs.append(log)

    # Creamos la instancia que se guardará en la base de datos
    report = Report(
        endpoint="/analysis",
        date=datetime.utcnow(),
        text=text,
        analysis=str(doc),
        execution_time=execution_time,
    )

    # Añadimos el reporte a la db
    db.add(report)
    db.commit()

    print(doc["entities"])

    if not doc["entities"]:
        doc["entities"] = [{"entity": "Verifica que el texto enviado sea un texto jurídico!"}]

    return doc

class Report(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    endpoint: str
    date: datetime
    text: str
    analysis: str
    execution_time: float

@app.get("/reports")
def generate_report():
    if not execution_logs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Por el momento no existen reportes!"
        )

    csv_file_path = "text_analysis_report.csv"

    with open(csv_file_path, mode="w", newline="") as csv_file:
        fieldnames = execution_logs[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(execution_logs)

    return FileResponse(csv_file_path, filename="text_analysis_report.csv", media_type="text/csv")