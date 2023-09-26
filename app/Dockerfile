FROM python:3.7

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY src/ /app/

WORKDIR /app

CMD ["uvicorn", "app:app", "--host=0.0.0.0"]