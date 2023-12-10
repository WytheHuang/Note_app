FROM python:3.11

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

EXPOSE 5000

CMD ["python", "run_asgi.py"]
