from airflow import DAG
import time
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='logrotate', schedule_interval='10 0 * * *', start_date=datetime(2020, 1, 1), catchup=False) as dag:
    
    # Task 1
    dummy_task = DummyOperator(task_id='dummy_task')
    
    # Task 2
    bash_task = BashOperator(task_id='rotateBotLogFile', bash_command="/usr/bin/python3 /home/guy/Documents/rotateLogFile.py")

    dummy_task >> bash_task
