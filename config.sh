# Setting up Airflow constants and configs

export AIRFLOW_HOME=~/airflow/airflow_works/
# This generates a skeleton airflow folder in AIRFLOW_HOME
airflow initdb
# creating airflow_works sub-folder's plugins and dags
mkdir -p ~/airflow/airflow_works/plugins
mkdir -p ~/airflow/airflow_works/dags
AIRFLOW_WORKS_DBURL=${AIRFLOW_WORKS_DBURL:-"postgres://localhost:5432/airflow_works"}  # Don't overwrite an existing value
export AIRFLOW_WORKS_POSTGRES_DBURL=${AIRFLOW_WORKS_DBURL}/postgres

# Linking this repo's airflow.cfg to the local airflow directory
CURRENT_DIR=`pwd`
LOCAL_AIRFLOW_CONFIG_PATH="CURRENT_DIR/setup/airflow.cfg"
# 1. Check if a local config file (not link) exists
# 2. If no local config create a link
if [ -e $LOCAL_AIRFLOW_CONFIG_PATH ]; then
    echo "Local custom Airflow config already exists."
else
    ln -s $CURRENT_DIR/setup/airflow.cfg.template $LOCAL_AIRFLOW_CONFIG_PATH
    echo "Linked airflow_works/setup/airflow.cfg to clover_config/dev/airflow.cfg.template."
fi
ln -sf $CURRENT_DIR/setup/airflow.cfg ~/airflow/airflow_works/airflow.cfg

python3 setup/airflow_setup.py # Creates symlinks between the files