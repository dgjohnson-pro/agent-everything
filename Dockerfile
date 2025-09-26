FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    PYTHONUNBUFFERED=1 \
    OLLAMA_URL=http://ollama:11434 \
    MODEL=llama3.2:latest \
    SYSTEM_PROMPT="You are a precise reasoning agent. Explain steps and prefer tool calls over guessing."

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
