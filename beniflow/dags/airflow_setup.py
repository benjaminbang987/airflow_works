"""

Setup file for airflow essentials. Package import, database import.

Code that goes along with the Airflow tutorial located at:
https://github.com/apache/airflow/blob/master/airflow/example_dags/tutorial.py

"""

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.sensors import HttpSensor
from datetime import datetime, timedelta
from airflow import models as af_models
import logging
import os
import subprocess
from beniflow.dags.tasks import game_1 as g1
from beniflow.dags.tasks import cms_data_pull as cdp
from beniflow.dags.constants import constants


START_DATE = datetime(2019, 4, 5, 10, 0, 0)
SCHEDULE_INTERVAL = "0 10 * * *"

dag_game_1 = af_models.DAG(
    dag_id="Beniflow",
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

t2 = PythonOperator(
    task_id='run_game_1_and_store_results',
    python_callable=g1.game_1_main,
    op_kwargs={"db_url": "airflow_works",
               "db_url_full": constants.LOCAL_DB_URL,
               "n_players": 3,
               "n_games": 100},
    dag=dag_game_1)

p0 = PythonOperator(
    # pulls the data from https://data.cms.gov/Medicare-Part-D/Medicare-Provider-Utilization-and-Payment-Data-201/yvpj-pmj2
    task_id='cms_data_pull',
    python_callable=cdp.run_cms_data_pull,
    op_kwargs={"website_link": "data.cms.gov",
               "token": None,
               "dataset_identifier": "xbte-dn4t",
               "crawl_limit": 5000,
               "db_url_full": constants.LOCAL_DB_URL,
               "db_url": "airflow_works",
               "schema": "sandbox",
               "table_name": "cms_drug_file"},
    dag=dag_game_1)

s1 = HttpSensor(
    task_id='http_sensor_check',
    http_conn_id='http_default',
    endpoint='',
    request_params={},
    response_check=lambda response: True if "Google" in response.text else False,
    dag=dag_game_1,
)

s2 = HttpSensor(
    task_id='cms_http_sensor',
    http_conn_id='cms_gov_http_id',
    endpoint='',
    request_params={},
    dag=dag_game_1,
)


t2.set_upstream(t1)
t1.set_upstream(s1)


def checks_airflow_home_dir():
    """
    Assumed default directory ($AIRFLOW_HOME) is used.
    If this is not existent, then function names AIRFLOW_HOME representing `~/airflow` directory for the user.
    """
    if subprocess.Popen('echo $AIRFLOW_HOME', stdout=subprocess.PIPE, shell=True
                        ).stdout.read().decode("utf-8").strip('\n'):
        af_home_dir = subprocess.Popen('echo $AIRFLOW_HOME', stdout=subprocess.PIPE, shell=True
                                       ).stdout.read().decode("utf-8").strip('\n')
    elif os.path.exists(os.path.expanduser('~/airflow/airflow_works')):
        subprocess.run('export AIRFLOW_HOME=~/airflow/airflow_works')
        logging.info("Initializing with the existing ~airflow/airflow_works as the AIRFLOW_HOME directory")
        af_home_dir = os.path.expanduser('~/airflow/airflow_works')
    else:
        af_home_dir = None
        AssertionError("Go back to the README and finish the Installation Requirements steps")
    return af_home_dir


def symbolic_link(src_path, trg_path):
    """
    Sets up a symbolic link between this DAG + any dependencies and the local directory for Airflow DAGs
    """
    if not os.path.exists(src_path):
        raise ValueError('Source path {src_path} does not exist'.format(src_path=src_path))
    if not os.path.exists(os.path.dirname(trg_path)):
        raise ValueError('Target path {trg_path} does not exist'.format(trg_path=trg_path))
    try:
        os.symlink(src=src_path, dst=trg_path)
    except FileExistsError:
        logging.info("DAG in %s is already connected to %s", src_path, trg_path)


if __name__ == "__main__":
    home_dir = checks_airflow_home_dir()
    symbolic_link(os.path.dirname(os.path.realpath(__file__)) + "/airflow_setup.py", home_dir + "dags/airflow_setup.py")
    symbolic_link(os.path.dirname(os.path.realpath(__file__)) + "/tasks/", home_dir + "dags/tasks")
    symbolic_link(os.path.dirname(os.path.realpath(__file__)) + "/airflow.cfg", home_dir + "airflow.cfg")