from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import time
from tasks.wmata_bus_position import main as wmata_bus
from tasks.wmata_train_position import main as wmata_train
from tasks.wmata_train_predictions import main as wmata_train_pred

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

dag = DAG('transit_v1', default_args=default_args, schedule_interval=timedelta(seconds=60))

def sleep():
	n = 9
	time.sleep(n)
	return n



execution = []
for i in range(0,6):
	execution.append(PythonOperator(dag=dag,
            task_id='call_wmata_bus_{}'.format(i),
            provide_context=False,
            python_callable=wmata_bus))
	execution.append(PythonOperator(dag=dag,
            task_id='call_wmata_train_{}'.format(i),
            provide_context=False,
            python_callable=wmata_train))
	if i == 0:
		execution.append(PythonOperator(dag=dag,
		    task_id='call_wmata_train_pred_{}'.format(i),
		    provide_context=False,
		    python_callable=wmata_train_pred))
	if i != 5:
		execution.append(PythonOperator(dag=dag,
			    task_id='sleep_9s_{}'.format(i),
			    provide_context=False,
			    python_callable=sleep))


# Add downstream
for i,val in enumerate(execution[:-1]):
    val.set_downstream(execution[i+1])

