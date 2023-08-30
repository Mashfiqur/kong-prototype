FROM python:latest

WORKDIR /app
COPY . .

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

EXPOSE 5000
CMD ["python", "main.py"]