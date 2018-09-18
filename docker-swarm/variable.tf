variable "aws_region" {
  description = "AWS region on which we will setup the swarm cluster"
  default = "eu-west-1"
}

variable "ami" {
  description = "Amazon Linux AMI"
  default = "ami-0bdb1d6c15a40392c"
}

variable "instance_type" {
  description = "Instance type"
  default = "t2.micro"
}

variable "key_path" {
  description = "SSH Public Key path"
  default = "./id_rsa.pub"
}

variable "key_name" {
  description = "Desired name of Keypair..."
  default = "swarm_keyname"
}

variable "bootstrap_path" {
  description = "Script to install Docker Engine"
  default = "install_docker.sh"
}
