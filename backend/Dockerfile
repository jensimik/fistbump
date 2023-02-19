
FROM python:3.10-slim-bullseye

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY fistbump /code/fistbump
COPY ./setup.json /code

CMD ["uvicorn", "fistbump.main:app", "--host", "0.0.0.0", "--port", "80"]