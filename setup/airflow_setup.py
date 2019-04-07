"""

Setup file for airflow essentials. Package import, database import.

Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
All rights reserved to the github repo above.

"""

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow import models as af_models

from tasks import game_1 as g1

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 3, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG('tutorial', default_args=default_args, schedule_interval=timedelta(days=1))


START_DATE = datetime.datetime(2017, 12, 5, 10, 0, 0)
SCHEDULE_INTERVAL = "0 10 * * *"
DEFAULT_ARGS = defaults.dag_default_args(
    notification_handlers=None, execution_timeout=datetime.timedelta(hours=2), retries=1
)

dag_game_1 = af_models.DAG(
    dag_id="rock_paper_scissors",
    default_args=DEFAULT_ARGS,
    start_date=START_DATE,
    schedule_interval=SCHEDULE_INTERVAL,
    catchup=False,
    concurrency=1,
    max_active_runs=1,
)
# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag)

t2 = BashOperator(
    task_id='sleep',
    bash_command='sleep 5',
    retries=3,
    dag=dag)

t4 = PythonOperator(
    python_callable=g1.rock_paper_scissors,
    op_kwargs={"n_players": 2, "n_rounds": 10}

)

templated_command = """
    {% for i in range(5) %}
        echo "{{ ds }}"
        echo "{{ macros.ds_add(ds, 7)}}"
        echo "{{ params.my_param }}"
    {% endfor %}
"""

t3 = BashOperator(
    task_id='templated',
    bash_command=templated_command,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t1)