FROM python:3.10-slim

WORKDIR /app
COPY ../requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000 
# CMD ["python", "run.py"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--reload"]
