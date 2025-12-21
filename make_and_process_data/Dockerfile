FROM python:3.12-slim

WORKDIR /app

COPY src/data ./src/data
COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD python ./src/data/preprocessing.py && tail -f /dev/null
