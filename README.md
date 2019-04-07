# airflow_works

## Workspace for creating a sample DAG using several tasks
## (As of 2019 April 01)

#### Steps taken: 

1. Follow the instructions here: http://airflow.apache.org/start.html
    1. Creating a setup for a sample DAG (follow through all the instructions to install pre-req packages)
    2. Create a PostgreSQL databse ([follow steps here](https://www.codementor.io/engineerapart/getting-started-with-postgresql-on-mac-osx-are8jcopb)) (in my case, I called it `airflow_works`)
    3. Create a new user with a new password
    4. Test run the DAG using localhost:8080, and create a new connection for the database created
2. Create tasks in a sample DAG
    1. Created a game (rock-paper-scissors) that spit out the results
    2. Wanted to run the game everyday and store the results with timestamp in the database using Airflow
3. (WIP) Create unit tests for tasks in a sample DAG
    1. Unit-testing the functionality of the rock-paper-scissors game
    2. Validation test framework for result logs coming out from the game

    
