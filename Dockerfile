FROM python:3.11-slim
WORKDIR /app
COPY agent/requirements.txt .
RUN pip install -r requirements.txt
COPY agent/agent.py .
CMD ["python", "agent.py"]