FROM python:3.8.6-buster

COPY . .

COPY requirements.txt /requirements.txt
COPY dataqc/abrolhos_qc.csv /abrolhos_qc.csv
COPY dataqc/alcatrazes_qc.csv /alcatrazes_qc.csv
COPY dataqc/imbituba_qc.csv /imbituba_qc.csv
COPY dataqc/noronha_qc.csv /noronha_qc.csv

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD uvicorn test_api.api:app --host 0.0.0.0 --port $PORT
