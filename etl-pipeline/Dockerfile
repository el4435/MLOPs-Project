FROM python:3.11

RUN pip install pandas pyarrow prometheus_client

WORKDIR /data

COPY . .

CMD ["python", "process_taxi.py"]
