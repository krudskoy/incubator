import os
import subprocess
import time

#Start is temporarily canceled
os.system('sudo nohup python server.py &> /dev/null &')

while True:

    os.system('sudo git fetch')


    local_repo = subprocess.Popen(["sudo git rev-parse HEAD"], stdout=subprocess.PIPE, shell=True)
    (local_out, local_err) = local_repo.communicate()

    remote_repo = subprocess.Popen(["sudo git rev-parse @{u}"], stdout=subprocess.PIPE, shell=True)
    (remote_out, remote_err) = remote_repo.communicate()


    if local_out != remote_out:
        os.system('sudo git pull origin master')
        f = open("server_pid","r")
        line = f.readlines()
        os.system('sudo kill ' +(line[0]))
        os.system('sudo nohup python server.py &> /dev/null &')

    time.sleep(3)
