from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from datetime import datetime

with DAG(
    dag_id="dataops_cleaning_dag",
    start_date=datetime(2025, 12, 1),
    schedule=None,
    catchup=False,
    tags=["dataops", "spark"]
) as dag:

    run_spark_job = SSHOperator(
        task_id="run_spark_cleaning_job",
        ssh_conn_id="spark_ssh",
        command="""
        /opt/spark/bin/spark-submit \
        /opt/airflow/spark_jobs/clean_transactions.py
        """
    )

    run_spark_job

