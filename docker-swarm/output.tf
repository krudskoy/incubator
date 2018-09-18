output "master_public_ip" {
    value = ["${aws_instance.swarm_master.public_ip}"]
}

output "worker1_public_ip" {
    value = ["${aws_instance.swarm_worker.public_ip}"]
}
