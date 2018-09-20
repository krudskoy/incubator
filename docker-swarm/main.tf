provider "aws" {
}

resource "aws_key_pair" "swarm_keypair"{
  key_name = "swarm_keypair"
  public_key = "${file("${var.key_path}")}"
}

resource "aws_instance" "swarm_master" {
  ami = "${var.ami}"
  instance_type = "${var.instance_type}"
  key_name = "${aws_key_pair.swarm_keypair.id}"
  user_data = "${file("${var.bootstrap_path}")}"
  vpc_security_group_ids = ["${aws_security_group.sgswarm.id}"]

tags {
    Name  = "swarm_master"
    swarm_type = "master"
  }
}

resource "aws_instance" "swarm_worker" {
  ami = "${var.ami}"
  instance_type = "${var.instance_type}"
  key_name = "${aws_key_pair.swarm_keypair.id}"
  user_data = "${file("${var.bootstrap_path}")}"
  vpc_security_group_ids = ["${aws_security_group.sgswarm.id}"]

tags {
    Name  = "swarm_worker"
    swarm_type = "worker"
  }

provisioner "local-exec" {
        command = "sleep 90;ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook --private-key ./id_rsa -i tfparser.py playbook.yml"
    }
}
