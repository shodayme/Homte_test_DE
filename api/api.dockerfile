FROM python:3.10.8-slim

WORKDIR /app
COPY api/api_requirements.txt .
RUN pip install  --no-cache-dir -r api_requirements.txt
COPY api/fetch_api.py .
COPY ../logger/loggerfactory.py ./logger/


ENTRYPOINT ["uvicorn", "fetch_api:create_app" , "--reload"]