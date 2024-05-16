import subprocess

python_files = ['layer.py', 'deploy_lambda.py']

for file in python_files:
    subprocess.run(['python', file], check=True)