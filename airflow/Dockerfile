FROM apache/airflow:2.8.2
RUN pip install apache-airflow==${AIRFLOW_VERSION}
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt