FROM python:3.11-slim
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# If you run FastAPI:
# CMD ["uvicorn", "ragchat:app", "--host", "0.0.0.0", "--port", "8080"]
# If your entrypoint is chat.py:
CMD ["python", "chat.py"]

