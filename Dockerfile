FROM python:3.10-slim

COPY requirements.txt /temp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /temp/requirements.txt

WORKDIR /app
COPY script.py .

CMD ["python", "script.py"]