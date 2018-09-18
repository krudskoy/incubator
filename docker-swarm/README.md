# Docker-swarm
Docker-swarm cluster with 1 master and 1 worker.

## How to use

### Export your credentials

```shell
export AWS_ACCESS_KEY_ID='your_access_key'
export AWS_SECRET_ACCESS_KEY='your_secret_key'
```
### Generate a keypair 

Generate a keypair and add a your public key's path to "variable.tf" file in appropriate section. 

```shell
variable "key_path" {
  description = "SSH Public Key path"
  default = "your_public_key_path"
}
```

### Execute the commands inside the dir

```shell
terraform init
terraform apply
ansible-playbook -i hosts playbook.yml
```
