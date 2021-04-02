from airflow import DAG
import os
import time
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='downloadXLS', schedule_interval='0 1 * * *', start_date=datetime(2020, 1, 1), catchup=False) as dag:
    
    # Task 1
    dummy_task = DummyOperator(task_id='dummy_task')
    
    # Task 2
    bash_task = BashOperator(task_id='xls', bash_command="/usr/bin/bash ~/Documents/downloadAntennas.sh ")

    dummy_task >> bash_task
