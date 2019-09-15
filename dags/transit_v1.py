from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from tasks.wmata_bus_position import main as wmata_bus

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 8, 10),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5),
    'execution_timeout': timedelta(seconds=60),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('transit_v1', default_args=default_args, schedule_interval=timedelta(seconds=10))

t1 = PythonOperator(dag=dag,
            task_id='call_wmata_bus',
            provide_context=False,
            python_callable=wmata_bus)


