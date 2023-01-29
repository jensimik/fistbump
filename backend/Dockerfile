
FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code
COPY ./tasks.py /code
COPY ./setup.json /code

#CMD ["gunicorn", "-w", "2", "--bind=0.0.0.0:80", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--loop", "asyncio", "--workers", "1", "--limit-concurrency", "100", "--limit-max-requests", "100"]