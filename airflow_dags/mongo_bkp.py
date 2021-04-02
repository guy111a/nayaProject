from airflow import DAG
import os
import time
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='mongoDB_backUp', schedule_interval='0 2 * * *', start_date=datetime(2020, 1, 1), catchup=False) as dag:
    
    # Task 1
    dummy_task1 = DummyOperator(task_id='dummy_task1')
    
    # Task 2
    bash_task = BashOperator(task_id='mongoDB', bash_command="/usr/bin/bash /home/guy/Documents/mongoBkp.sh ")

    dummy_task1 >> bash_task
