'''
Script to get data from datalake curated layer for redshift

Author: Vitor Abdo
Date: June/2023
'''

# import necessary packages
import psycopg2

def create_redshift_table(
        redshift_config: dict, table_name: str, column_definitions: list) -> None:
    '''
    Create a table in Amazon Redshift if it doesn't exist.

    Args:
        redshift_config (dict): Configuration parameters for the Redshift connection.
        table_name (str): Name of the table to be created.
        column_definitions (list): List of dictionaries defining the columns and their data types.

    Returns:
        None
    '''

    # Redshift Configuration
    redshift_host = redshift_config['host']
    redshift_port = redshift_config['port']
    redshift_database = redshift_config['database']
    redshift_user = redshift_config['user']
    redshift_password = redshift_config['password']

    # Establish a connection to Redshift
    conn = psycopg2.connect(
        host=redshift_host,
        port=redshift_port,
        database=redshift_database,
        user=redshift_user,
        password=redshift_password
    )

    # Check if the table already exists
    with conn.cursor() as cursor:
        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = %s)", (table_name,))
        table_exists = cursor.fetchone()[0]

        # Create the table if it doesn't exist
        if not table_exists:
            create_table_query = f"CREATE TABLE {table_name} ("
            for i, column in enumerate(column_definitions):
                column_name = column['name']
                column_type = column['type']
                create_table_query += f"{column_name} {column_type}"
                if i < len(column_definitions) - 1:
                    create_table_query += ","
            create_table_query += ")"
            cursor.execute(create_table_query)
            conn.commit()

    # Close the connection to Redshift
    conn.close()

# Redshift Configuration
redshift_config = {
    'host': 'default.413301752162.us-east-1.redshift-serverless.amazonaws.com',
    'port': '5439',
    'database': 'dev',
    'user': 'brand_data_storage',
    'password': 'y!Wj3Z7ZCE99ngX'
}

# Define the table name and column definitions
table_name = 'curated_official_page_tweets'
column_definitions = [
    {'name': 'tweet_id', 'type': 'text'},
    {'name': 'created_at', 'type': 'timestamp'},
    {'name': 'text', 'type': 'text'},
    {'name': 'retweets', 'type': 'integer'},
    {'name': 'likes', 'type': 'integer'},
    {'name': 'id', 'type': 'text'},
    {'name': 'ran_at', 'type': 'timestamp'},
    {'name': 'updated_at', 'type': 'timestamp'},
    {'name': 'year', 'type': 'integer'},
    {'name': 'month', 'type': 'integer'},
    {'name': 'day', 'type': 'integer'},
    {'name': 'hour', 'type': 'integer'},
    {'name': 'day_of_week', 'type': 'integer'}
]

# Call the function to create the table if it doesn't exist
create_redshift_table(redshift_config, table_name, column_definitions)