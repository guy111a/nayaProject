from airflow import DAG
import time
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='move2GPC', schedule_interval='20 0 * * *', start_date=datetime(2020, 1, 1), catchup=False) as dag:
    
    # Task 1
    dummy_task = DummyOperator(task_id='dummy_task')
    
    # Task 2
    bash_task = BashOperator(task_id='toGCP', bash_command="/usr/bin/python3 /home/guy/Documents/move2gcp.py")

    dummy_task >> bash_task
