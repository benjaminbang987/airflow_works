# Setting up Airflow constants and configs

mkdir -p ~/airflow/airflow_works
export AIRFLOW_HOME=~/airflow/airflow_works/
AIRFLOW_WORKS_DBURL=${AIRFLOW_WORKS_DBURL:-"postgres://localhost:5432/airflow_works"}  # Don't overwrite an existing value
export AIRFLOW_WORKS_POSTGRES_DBURL=${AIRFLOW_WORKS_DBURL}/postgres