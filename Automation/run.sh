sudo snap install aws-cli --classic
sudo snap install terraform --classic
sudo apt install ansible

export $(cat .env | xargs)

cd terraform
terraform init
terraform apply -auto-approve
# terraform refresh
terraform output -raw hosts > ../ansible/inventory/hosts.json

cd ../ansible
ansible-playbook playbooks/update.yml
ansible-playbook playbooks/docker.yml
ansible-playbook playbooks/airbyte.yml
ansible-playbook playbooks/metabase.yml

cd ../lambda
aws configure set aws_access_key_id "$TF_VAR_AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$TF_VAR_AWS_SECRET_ACCESS_KEY"
aws configure set region "$AWS_REGION"
aws configure set output "text"

python3 main.py