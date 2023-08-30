FROM python:latest

WORKDIR /cdn
COPY . .

RUN pip install --upgrade pip
RUN pip install -r /cdn/requirements.txt

EXPOSE 5001
CMD ["python", "main.py"]