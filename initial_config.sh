# Initial setup of Airflow_works pyenv and package requirements

pip install -r requirements.txt
pyenv virtualenv 3.6.2 airflow_works
pyenv activate airflow_works
pyenv local airflow_works # this takes care of the local fixation