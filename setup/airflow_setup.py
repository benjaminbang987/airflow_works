"""

Setup file for airflow essentials. Package import, database import.

Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py
All rights reserved to the github repo above.

"""

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow import models as af_models

from tasks import game_1 as g1


START_DATE = datetime(2019, 4, 5, 10, 0, 0)
SCHEDULE_INTERVAL = "0 10 * * *"

dag_game_1 = af_models.DAG(
    dag_id="rock_paper_scissors",
    default_args={"notification_handlers": None,
                  "execution_timeout": timedelta(hours=2),
                  "retries": 1},
    start_date=START_DATE,
    schedule_interval=SCHEDULE_INTERVAL,
    catchup=False,
    concurrency=1,
    max_active_runs=1,
)

t1 = BashOperator(
    task_id='print_date',
    bash_command='date',
    dag=dag_game_1)

t4 = PythonOperator(
    python_callable=g1.game_1_main,
    op_kwargs={"database_url": "airflow_works",
               "n_players": 3,
               "n_rounds": 100},
    dag=dag_game_1)
