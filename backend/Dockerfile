
FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code
COPY ./tasks.py /code
COPY ./setup.json /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "1", "--limit-concurrency", "100"]