FROM python:3.10.8-slim

WORKDIR /app
COPY api_requirements.txt .
RUN pip install -r api_requirements.txt
COPY fetch_api.py .
COPY ../logger/loggerfactory.py ./logger/


ENTRYPOINT ["uvicorn", "api:fast_app" , "--reload"]