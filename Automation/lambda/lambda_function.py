import snowflake.connector as sf
import os
import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# --> Download data from URL ----------------------------------------------------------
def download_data(url, destination_folder, file_name):
    
    local_file_path = os.path.join(destination_folder, file_name)
    logger.info(f"Downloading data from {url} to {local_file_path}")
    
    response = requests.get(url)
    response.raise_for_status()
    
    with open(local_file_path, "wb") as file:
        file.write(response.content)
        
    return local_file_path

# --> Upload data to Snowflake ----------------------------------------------------------
def upload_to_snowflake(local_file_path):
    logger.info(f"Uploading data from {local_file_path} to Snowflake")
    
    schema = os.environ["schema"]
    stage = os.environ["stage"]
    table = os.environ["table"]
    
    conn = sf.connect(
        user =      os.environ["user"],
        password =  os.environ["password"],
        account =   os.environ["account"],
        warehouse = os.environ["warehouse"],
        database =  os.environ["database"],
        schema =    schema,
        role =      os.environ["role"],
    )
    cursor = conn.cursor()

    cursor.execute(f"USE SCHEMA {schema};")
    cursor.execute(f"PUT 'file://{local_file_path}' @{stage};")
    cursor.execute(f'TRUNCATE TABLE {schema}."{table}";')
    cursor.execute(
        f'COPY INTO {schema}."{table}" FROM @
        {stage}/{os.path.basename(local_file_path)} FILE_FORMAT =COMMA_CSV ON_ERROR = "CONTINUE";')

# --> Lambda handler function ----------------------------------------------------------
def lambda_handler(event, context):
    logger.info("Starting lambda_handler function")

    local_file_path = download_data(
        url= "https://de-materials-tpcds.s3.ca-central-1.amazonaws.com/inventory.csv",
        destination_folder= "/tmp",
        file_name= "inventory.csv",
    )

    upload_to_snowflake(local_file_path)

    logger.info("File downloaded and uploaded to Snowflake successfully.")
    return {
        "statusCode": 200,
        "body": "ALL DONE!",
    } 