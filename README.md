# airflow_works

## Workspace for creating a sample DAG using several tasks
## (As of 2019 April 01)

#### Packages

Python
To peg the pyenv and python setup, please create/activate a virtual environment for this repo as directed below:
```
pyenv virtualenv 3.6.2 airflow_works
pyenv activate airflow_works
```
Now that the virtual environment is setup, it's time to install package dependencies.
```
pip install -r pkg_requirements.txt
```

#### Steps taken for this project: 

1. Follow the instructions here: http://airflow.apache.org/start.html
    1. Creating a setup for a sample DAG (follow through all the instructions to install pre-req packages)
    2. Create a PostgreSQL databse ([follow steps here](https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb)) (in my case, I called it `airflow_works`)
    3. Create a new user with a new password
    4. Test run the DAG using localhost:8080, and create a new connection for the database created
2. Create tasks in a sample DAG
    1. Created a game (rock-paper-scissors) that spit out the results
    2. Run the game on demand and store the results with timestamp in the database using Airflow
3. (WIP) Create unit tests for tasks in a sample DAG
    1. Unit-testing the functionality of the rock-paper-scissors game
    2. Validation test framework for result logs coming out from the game
4. Create API connection for external data crawler


