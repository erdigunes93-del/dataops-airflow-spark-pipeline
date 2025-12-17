\# DataOps Assignment - Airflow + Spark Client



\## Overview

This project demonstrates a simple DataOps pipeline that ingests raw data from object storage, cleans it using Pandas/PySpark, and loads the processed data into PostgreSQL for analytical use.



\## Tech Stack

\- Airflow 3 (orchestration)

\- Spark Client (execution environment)

\- MinIO (object storage)

\- PostgreSQL (data warehouse)

\- GitHub + git-sync (CI/CD style deployment)



\## Pipeline Flow

1\. Raw data is stored in MinIO bucket `dataops-bronze` under `raw/dirty\_store\_transactions.csv`

2\. Data cleaning is performed using Pandas/PySpark running inside `spark\_client`

3\. Cleaned data is loaded into PostgreSQL database `traindb`, table `public.clean\_data\_transactions` (full load)

4\. Airflow triggers the Spark job using SSHOperator



