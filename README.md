# Brand Data Analysis

## Table of Contents

1. [Project Description](#description)
2. [Files Description](#files)
3. [Running Files](#running)
4. [Orchestration](#orchestration)
5. [Data Visualization](#visualization)
6. [Licensing and Authors](#licensingandauthors)
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

* `template.yaml`: AWS cloud formation instance template to create RDS, DMS and S3 services, integrating all of them.

* `main's files`: two main files in the main directory that manage all the functions that are in the *components* folder.

    * `main_load_to_rds.py`: Python script for running the data collection, transformation, and upload the transformed data into the RDS Postgres.
    * `main_s3_management.py`: Python script to manage all transformations of datalake layers in S3 bucket

* `components/`: Directory containing the modularized components for the project. The files listed here are more or less in the order they are called.

    * `extract_tweets.py`: Python module to collect data from twitter and read them as pandas dataframe.
    * `data_transform.py`: Python module for transforming the raw data into a format that can be loaded into the PostgreSQL database.
    * `data_load.py`: Python module for loading the transformed data into the PostgreSQL database.
    * `create_s3_raw_folder.py`: Python module to move the data that arrived in the staging bucket from the DMS to the raw layer.
    * `create_s3_processed_folder.py`: Python module to move data from raw layer to processed layer (performing some basic transformations).
    * `create_s3_curated_folder.py`: Python module to move the data from the processed layer to the curated layer (performing some major, business-specific transformations).

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

Go to [brand_data_analysis](https://github.com/vitorbeltrao/brand_data_analysis) and click on Fork in the upper right corner. This will create a fork in your Github account, i.e., a copy of the repository that is under your control. Now clone the repository locally so you can start working on it:

`git clone https://github.com/[your_github_username]/brand_data_analysis.git`

and go into the repository:

`cd brand_data_analysis` 

### Create AWS account

Go to the [AWS](https://aws.amazon.com/) page and create a free account for you to use the services needed for the project.

### .env File

To make everything work, you need to create the `.env` file in your main directory, so that *main's* files runs smoothly. 

In the .env, you must define all necessary variables like usernames, passwords and anything else that is sensitive information for your project.

### template.yaml File

Go to the [cloud formation](https://aws.amazon.com/cloudformation/) instance on AWS and upload this template so that the database, DMS and S3 services are created to start the pipeline.

### main.py File

After all the above steps, you can run it in your terminal (in the order), in your main directory: `python main_load_to_rds.py` and `python main_s3_management.py` to execute the components in order from the *components* folder.

### Testing

- Run the tests:

    `pytest`

    The tests of the functions used are in the `brand_data_analysis/tests` folder and to run them just write the code above in the terminal. In that folder are the tests that cover the production functions that are in the `brand_data_analysis/components` folder.
***

## Orchestration <a name="orchestration"></a>

The project uses a modularized approach for data collection, transformation, and loading. This approach allows for greater flexibility and scalability in the project. The main.py script orchestrates the execution of these modules.
***

## Data Visualization <a name="visualization"></a>

The data collected from twitter and passed for several transformations along the pipeline, based on various inputs from employees targeting different business rules, were made available in a dashboard by the [metabase](https://www.metabase.com/).

![Brand Analysis dashboard]()
***

## Licensing and Author <a name="licensingandauthors"></a>

Vítor Beltrão - Data Scientist

Reach me at: 

- vitorbeltraoo@hotmail.com

- [linkedin](https://www.linkedin.com/in/v%C3%ADtor-beltr%C3%A3o-56a912178/)

- [github](https://github.com/vitorbeltrao)

- [medium](https://pandascouple.medium.com)

Licensing: [MIT LICENSE](https://github.com/vitorbeltrao/populate_database/blob/main/LICENSE)