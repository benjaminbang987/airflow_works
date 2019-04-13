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
import os
import subprocess
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
    task_id='run_game_1_and_store_results',
    python_callable=g1.game_1_main,
    op_kwargs={"database_url": "airflow_works",
               "n_players": 3,
               "n_games": 100},
    dag=dag_game_1)


def checks_airflow_home_dir(manual_dir):
    if manual_dir:
    else:
        home_dir = subprocess.Popen('echo $AIRFLOW_HOME', stdout=subprocess.PIPE, shell=True).stdout.read().decode("utf-8").strip('\n')


def symbolic_link(src_path, trg_path):
    if not os.path.exists(src_path):
        raise ValueError('Source path {src_path} does not exist'.format(src_path=src_path))
    if not os.path.exists(os.path.dirname(trg_path)):
        raise ValueError('Target path {trg_path} does not exist'.format(trg_path=trg_path))
    try:
        os.symlink(src=src_path, dst=trg_path)
    except FileExistsError:
        print("DAG in {dag} is already connected to {trg_path}".format(dag=src_path,
                                                                       trg_path=trg_path))


if __name__ == "__main__":
    import pdb; pdb.set_trace()

    symbolic_link(os.path.dirname(os.path.realpath(__file__)) + "/airflow_setup.py",  + "/airflow_setup.py")

    symbolic_link(os.path.dirname(os.path.realpath(__file__)) + "/tasks/", "/Users/benjaminbang/airflow/dags/tasks")