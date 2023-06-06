# Brand Data Analysis

## Table of Contents

1. [Project Description](#description)
2. [Files Description](#files)
3. [Running Files](#running)
4. [Orchestration](#orchestration)
5. [Licensing and Authors](#licensingandauthors)
***

## Project Description <a name="description"></a>

This project aims to collect data from Twitter using the official API, store it in an RDS Postgres database, replicate the data to an S3 datalake, perform layered transformations within the datalake (raw, processed, curated), send the transformed data to Redshift (an AWS managed data warehouse), and connect Redshift to Metabase to deliver valuable insights and information through data analysis. 

**Goals:**

* Collect Twitter data using the official API.

* Store the collected data in an RDS Postgres database.

* Replicate the data to an S3 datalake.

* Perform layered transformations (raw, processed, curated) within the datalake.

* Send the transformed data to Redshift.

* Connect Redshift to Metabase to provide insights and information to end-users.

![Brand Analysis architecture](https://github.com/vitorbeltrao/brand_data_analysis/blob/main/images/brand_data_analysis_architecture.jpg?raw=true)
***

## Files Description <a name="files"></a>

* `docker-compose.yml`: Docker Compose file for creating the PostgreSQL database locally.

* `main.py`: Main Python script for running the data collection, transformation, and upload the transformed data, that is, all three components created in the *components* folder.

* `components/`: Directory containing the modularized components for the project.

    * `data_collector.py`: Python module to collect raw data from Kaggle and read it as a pandas dataframe.
    * `data_transform.py`: Python module for transforming the raw data into a format that can be loaded into the PostgreSQL database.
    * `data_load.py`: Python module for loading the transformed data into the PostgreSQL database.

* `tests/`: directory that contains the tests for the functions that are in `components/`.

    * `test_collector.py`: Unit tests for the functions of the respective component.
    * `test_transform.py`: Unit tests for the functions of the respective component.
    * `test_load.py`: Unit tests for the functions of the respective component.
    * `conftest.py`: File where the fixtures were created to feed the unit tests.

* `.env`: File containing environment variables used in the project.
***

## Running Files <a name="running"></a>

To run the project, follow these steps:

### Clone the repository

Go to [populate_database](https://github.com/vitorbeltrao/populate_database) and click on Fork in the upper right corner. This will create a fork in your Github account, i.e., a copy of the repository that is under your control. Now clone the repository locally so you can start working on it:

`git clone https://github.com/[your_github_username]/populate_database.git`

and go into the repository:

`cd populate_database` 

### Install Docker

On Windows, you will have to [install docker](https://docs.docker.com/desktop/install/windows-install/) to be able to run the database locally.

Once installed, you can run it in your terminal: `docker-compose up db` or `docker-compose up -d db` to start your database. To stop docker, just run it in your terminal: `docker-compose down`.

### .env File

To make everything work, you need to create the `.env` file in your main directory, so that *main.py* runs smoothly. 

In the .env, you must define the following variables:

* `HOST_NAME`: str (Name of your hostname)

* `PORT`: str (Number of port used for the protocol)

* `DB_NAME`: str (Name of your postgres database)

* `USER`: str (Name of postgres user)

* `PASSWORD`: str (The password of created database)

* `SCHEMAS_TO_CREATE`: Do not quote this variable (Name of the schemas you want to create, for example: *SCHEMAS_TO_CREATE = startups_hiring,nba*)

* `OPEN_POSITIONS_RAW_PATH`: str (Startups dataset path)

* `NBA_PAYROLL_RAW_PATH`, `NBA_PLAYER_BOX_RAW_PATH`, `NBA_PLAYER_STATS_RAW_PATH`, `NBA_SALARIES_RAW_PATH`: str (NBA datasets path)

### main.py File

After all the above steps, and with docker running, you can run it in your terminal, in your main directory: `python main.py` to execute the three components in order from the *components* folder.

### Testing

- Run the tests:

    `pytest`

    The tests of the functions used are in the `populate_database/tests` folder and to run them just write the code above in the terminal. In that folder are the tests that cover the production functions that are in the `populate_database/components` folder.
***

## Orchestration <a name="orchestration"></a>

The project uses a modularized approach for data collection, transformation, and loading. This approach allows for greater flexibility and scalability in the project. The main.py script orchestrates the execution of these modules.
***

## Licensing and Author <a name="licensingandauthors"></a>

Vítor Beltrão - Data Scientist

Reach me at: 

- vitorbeltraoo@hotmail.com

- [linkedin](https://www.linkedin.com/in/v%C3%ADtor-beltr%C3%A3o-56a912178/)

- [github](https://github.com/vitorbeltrao)

- [medium](https://pandascouple.medium.com)

Licensing: [MIT LICENSE](https://github.com/vitorbeltrao/populate_database/blob/main/LICENSE)