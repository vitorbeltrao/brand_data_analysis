# NASA Data Analysis - Asteroid data exploration - v0.0.1

## Table of Contents

1. [Project Description](#description)
2. [Files Description](#files)
3. [Running Files](#running)
4. [Orchestration](#orchestration)
5. [Data Visualization](#visualization)
6. [Licensing and Authors](#licensingandauthors)
***

## Project Description <a name="description"></a>

This project aims to collect data from the NASA official API (Asteroids - NeoWs), store it in an RDS Postgres database, replicate the data to a data lake in S3 using the AWS Database Migration Service (DMS), perform layered transformations within the data lake (raw and processed), and visualize the data using the Streamlit Python library. 

**The workflow includes the following steps:**

* Data Collection: Retrieve data from the NASA API using the provided endpoints.

* Data Storage: Store the collected data in an RDS Postgres database for persistent storage and easy retrieval.

* Data Replication: Use the AWS Database Migration Service (DMS) to replicate the data from the RDS Postgres database to a data lake in S3. This ensures that the data is available in the data lake for further processing and analysis.

* Data Transformations: Apply necessary transformations and processing to the data within the data lake, creating processed datasets.

* Send the transformed data to RDS Postgres as a data warehouse.

* Data Visualization: Utilize the Streamlit Python library to build interactive and informative data visualizations, enabling users to explore and analyze the processed datasets.

![architecture](https://github.com/vitorbeltrao/brand_data_analysis/blob/main/images/architecture.jpg?raw=true)

By incorporating the AWS Database Migration Service (DMS) for data replication, the project ensures efficient and reliable transfer of data from the RDS Postgres database to the data lake in S3, facilitating subsequent transformations and visualization using the Streamlit Python library.
***

## Files Description <a name="files"></a>

* `template.yaml`: AWS cloud formation instance template to create RDS, DMS and S3 services, integrating all of them.

* `main's files`: two main files in the main directory that manage all the functions that are in the *components* folder.

    * `main_load_to_rds.py`: Python script for running the data collection, transformation, and upload the transformed data into the RDS Postgres.
    * `main_s3_management.py`: Python script to manage all transformations of datalake layers in S3 bucket
    * `main_load_dw.py`: Python script to send the processed data from processed layer to a data warehouse, to improve the path to consult this data in a visualization tool, for example.
    * `hello.py`: main page of the streamlit app.

* `components/`: Directory containing the modularized components for the project. The files listed here are more or less in the order they are called.

    * `data_extract.py`: Python module to collect data from nasa (Asteroids - NeoWs) and read them as pandas dataframe.
    * `data_transform.py`: Python module for transforming the raw data into a format that can be loaded into the PostgreSQL database.
    * `data_load.py`: Python module for loading the transformed data into the PostgreSQL database.
    * `create_s3_raw_folder.py`: Python module to move the data that arrived in the staging bucket from the DMS to the raw layer.
    * `create_s3_processed_folder.py`: Python module to move data from raw layer to processed layer (performing some basic transformations).
    * `get_processed_s3_data.py`: Python module to retrieve the data from the processed layer.

* `pages/`: directory that contains the streamlit pages to delivery to the customers.

    * `exploratory_data_analysis.py`: Python script that we made our dashboard from the data.

* `tests/`: directory that contains the tests for the functions that are in `components/`.

    * `test_collector.py`: Unit tests for the functions of the respective component (data_extract.py).
    * `test_transform.py`: Unit tests for the functions of the respective component (data_transform.py).
    * `test_load.py`: Unit tests for the functions of the respective component (data_load.py).
    * `conftest.py`: File where the fixtures were created to feed the unit tests.

* `.env`: File containing environment variables used in the project.
***

## Running Files <a name="running"></a>

To run the project, follow these steps:

### Clone the repository

Go to [nasa_data_analysis](https://github.com/vitorbeltrao/nasa_data_analysis) and click on Fork in the upper right corner. This will create a fork in your Github account, i.e., a copy of the repository that is under your control. Now clone the repository locally so you can start working on it:

`git clone https://github.com/[your_github_username]/nasa_data_analysis.git`

and go into the repository:

`cd nasa_data_analysis` 

### Create AWS account

Go to the [AWS](https://aws.amazon.com/) page and create a free account for you to use the services needed for the project.

### template.yaml File

Go to the [cloud formation](https://aws.amazon.com/cloudformation/) instance on AWS and upload this template so that the database, DMS and S3 services are created to start the pipeline.

After everything is created, including the postgres RDS instance, you must access the database and run this code: `create extension pglogical`

### main's Files

After all the above steps, you can run it in your terminal (in the order), in your main directory: `python main_load_to_rds.py`, `python main_s3_management.py` and `python main_load_dw.py` to execute the components in order from the *components* folder. This will run all the necessary pipeline (in order) to get the data into the database, then make the necessary transformations inside the data lake, and finally push the transformed data up to a data warehouse.

### Stremlit app

To run streamlit locally, just run: `streamlit run hello.py` and then a web browser will load the service and you can enjoy the dashboard. To deploy and make it available to anyone through a link, you must register on the [site](https://streamlit.io/) and follow the step by step.

### .env File

To make everything work, you need to create the `.env` file in your main directory, so that *main's* files runs smoothly. 

In the .env, you must define all necessary variables like usernames, passwords and anything else that is sensitive information for your project.

### Testing

- Run the tests:

    `pytest`

    The tests of the functions used are in the `brand_data_analysis/tests` folder and to run them just write the code above in the terminal. In that folder are the tests that cover the production functions that are in the `brand_data_analysis/components` folder.
***

## Orchestration <a name="orchestration"></a>

The project uses a modularized approach for data collection, transformation, and loading. This approach allows for greater flexibility and scalability in the project. The main.py script orchestrates the execution of these modules.
***

## Data Visualization <a name="visualization"></a>

The data collected from the NASA API and processed through various transformations in the pipeline, incorporating different business rules and inputs from employees, will be presented in a dashboard using the Streamlit library. This dashboard will provide an interactive and user-friendly interface to visualize and explore the NASA data. Streamlit is a powerful Python library for building data applications and interactive visualizations, allowing users to gain valuable insights from the collected and curated data.

Here is the link to the dashboard implemented and available to anyone: (in progress...)
***

## Licensing and Author <a name="licensingandauthors"></a>

Vítor Beltrão - Data Scientist

Reach me at: 

- vitorbeltraoo@hotmail.com

- [linkedin](https://www.linkedin.com/in/v%C3%ADtor-beltr%C3%A3o-56a912178/)

- [github](https://github.com/vitorbeltrao)

- [medium](https://pandascouple.medium.com)

Licensing: [MIT LICENSE](https://github.com/vitorbeltrao/populate_database/blob/main/LICENSE)