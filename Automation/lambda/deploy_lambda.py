import boto3
import os
import yaml

# Load the YAML file
with open('../config.yaml', 'r') as file:
    var = yaml.safe_load(file)    

def create_lambda_function():
    environment_variables = {
    'user' : os.getenv(var['snowflake']['user']),
    'password' : os.getenv(var['snowflake']['password']),
    'account' : var['snowflake']['account'],
    'warehouse' : var['snowflake']['warehouse'],
    'database' : var['snowflake']['database'],
    'role' : var['snowflake']['role'],
    'schema' : var['snowflake']['schema'],
    'stage' : var['snowflake']['stage'],
    'table' : var['snowflake']['table']
    }
    
    lambda_client = boto3.client("lambda")
    
    response = lambda_client.create_function(
       
        FunctionName=var['lambda']['function_name'],
        Runtime= var['lambda']['runtime'],
        Handler="lambda_function.lambda_handler",
        MemorySize = var['lambda']['memory_size'],
       
        Code={
            "S3Bucket": var['aws']['s3_bucket'],
            "S3Key": f"lambda_functions/{var['lambda']['function_name']}.zip",
        },
        
        Role=f"arn:aws:iam::{var['aws']['user_id']}:role/{var['lambda']['role']}",
        Layers = [f"arn:aws:lambda:{var['aws']['location']}:{var['aws']['user_id']}:layer:{pkg['name']}:{pkg['version']}" for pkg in var['lambda']['packages']], 
        
        Timeout=var['lambda']['timeout'],
        Environment = {
            'Variables' : environment_variables
        }
        )
    
    print("Lambda function created successfully")


def create_eventbridge_rule():
    eventbridge_client = boto3.client("events")
    lambda_client = boto3.client("lambda")
    
    response = eventbridge_client.put_rule(
        Name=var['event']['name'],
        Description=var['event']['description'],
        ScheduleExpression= "cron(0 23 * * ? *)",
    )

    response = eventbridge_client.put_targets(
        Rule= var['event']['name'],
        Targets=[
            {
                "Arn": f"arn:aws:lambda:{var['aws']['location']}:{var['aws']['user_id']}:function:{var['lambda']['function_name']}",
                "Id": "target1",
            }
        ],
    )

    response = lambda_client.add_permission(
        FunctionName=var['lambda']['function_name'],
        StatementId="1",
        Action="lambda:InvokeFunction",
        Principal="events.amazonaws.com",
        SourceArn=f"arn:aws:events:{var['aws']['location']}:{var['aws']['user_id']}:rule/{var['event']['name']}",
    )

    print("EventBridge rule created successfully")


if __name__ == "__main__":
    os.system(f"zip {var['lambda']['function_name']}.zip lambda_function.py")
    
    s3 = boto3.client("s3")
    s3.upload_file(
        f"{var['lambda']['function_name']}.zip",
        var['aws']['s3_bucket'],
        f"lambda_functions/{var['lambda']['function_name']}.zip",
    )
    
    create_lambda_function()
    create_eventbridge_rule()

os.remove(f"{var['lambda']['function_name']}.zip")