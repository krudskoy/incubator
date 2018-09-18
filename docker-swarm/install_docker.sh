#!/bin/sh
sudo yum update
sudo yum install -y docker
sudo systemctl start docker
usermod -aG docker ec2-user
