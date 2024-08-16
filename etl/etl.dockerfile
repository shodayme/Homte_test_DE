FROM python:3.10.8-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY etl.py .
COPY ../logger/loggerfactory.py ./logger/
COPY ../data ./data/

ARG INPUT_PATH
ENV INPUT_PATH=${INPUT_PATH}

COPY ${INPUT_PATH} ${INPUT_PATH}

ENTRYPOINT python etl.py -p ${INPUT_PATH} -l ./logs/etl_logs.log

