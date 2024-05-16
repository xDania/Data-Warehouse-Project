import os
import boto3
import shutil
import yaml

# Load the YAML file
with open('../config.yaml', 'r') as file:
    var = yaml.safe_load(file)
    
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

for package in var['lambda']['packages']:
    
    package_name = package['name']

    # Install package as a zip file
    if os.path.exists("python"):
        shutil.rmtree("python")
    os.makedirs("python")

    if package_name == 'snowflake-connector-python':
        os.system(f"pip3 install --platform manylinux2010_x86_64 --implementation cp --python 3.9 --only-binary=:all: --upgrade --target python/ snowflake-connector-python==2.7.9")
    else:
        os.system(f"pip3 install {package_name} -t python")

    zip_file = f"{package_name}.zip"
    os.system(f"zip -r {zip_file} python")

    # Upload layer.zip to AWS
    file_path = f"layers/{zip_file}"
    s3_client.upload_file(zip_file, var['aws']['s3_bucket'], file_path)

    response = lambda_client.publish_layer_version(
        LayerName=package_name,
        Content={
            "S3Bucket": var['aws']['s3_bucket'],
            "S3Key": file_path,
        },
        CompatibleRuntimes=[var['lambda']['runtime']],
    )

    package['version'] = response['Version']
    
    os.remove(f'{package_name}.zip')
shutil.rmtree("python")

# Write the updated YAML file
with open('../config.yaml', 'w') as file:
    yaml.dump(var, file, default_flow_style=False)