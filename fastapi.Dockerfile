FROM python:3.9.9

EXPOSE 9000

WORKDIR /opt/server

RUN pip install jina==3.6.3 docarray==0.13.22 fastapi uvicorn pydantic boto3

COPY main.py model.py s3.py /opt/server/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
