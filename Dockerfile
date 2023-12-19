FROM python:3.11-slim

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV PORT 8000

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# COPY .env /app/
COPY src /app/src
# COPY db.sqlite3 /app/db.sqlite3
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT}
