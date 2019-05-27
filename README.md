# airflow_works

## Workspace for creating a sample DAG using several tasks
## (2019 April 01 ~)

#### Installation Requirements

Creating a virtual environment for this repo, as well as downloading the initial package requirements can be done via the following code:
  
```
source initial_config.sh
```

Next, we need to initialize the database. Run the following to initialize the database:
    ```
    psql postgres
    ```
Once you are in the SQL shell, run
```
CREATE DATABASE airflow_works;
```
Run `\l` to check that the database is created.  

Next, run this whenever you are in this repo to reset the Airflow constants:

```
source config.sh
```

As a validation setp, run the terminal window run `echo $AIRFLOW_WORKS_DBURL` to see if the Airflow config is linked to the correct database. 
The name of the database should be equal to the name after the `postgres://localhost:port_number/`.
Run `psql $AIRFLOW_WORKS_DBURL` to see if you can psql into the database. If you can, `\q` out from the
sql shell and you are ready to roll.

#### Exact steps to locally run Airflow

- Follow through on the installation requirements set above.
- After the database is correctly setup and linked to the Airflow via a config, 
open a terminal window with the correct pyenv, run 
    ```
    airflow webserver -p 8080
    ```
- Open another terminal window with correct the correct pyenv (will be automated), run 
    ```
    airflow scheduler
    ```
- 

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
    1. Read https://dev.socrata.com/consumers/getting-started.html for starters on Socrata API.
    2. Setup API for data from https://data.cms.gov/browse?q=Medicare%20Provider%20Utilization%20and%20Payment%20Data%3A%202015%20Part%20D%20Prescriber&sortBy=relevance (relevant to https://github.com/sfbrigade/datasci-open-payments)
5. Read up [Definition of ETL](https://databricks.com/glossary/extract-transform-load)


#### Useful Articles on Airflow

Vineet Goel (Robinhood): (Why Robinhood Uses Airflow)[https://robinhood.engineering/why-robinhood-uses-airflow-aed13a9a90c8]

()Useful Quora for .bashrc/.bash_profile)[https://www.quora.com/What-is-bash_profile-and-what-is-its-use]