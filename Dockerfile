FROM python:3.11-slim

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV PORT 8000

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# COPY .env /app/
COPY src /app/src

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN python -m spacy download es_core_news_md

CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT}
