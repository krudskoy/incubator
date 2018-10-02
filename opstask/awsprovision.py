from botocore.exceptions import ClientError
import paramiko
import boto3
import time
import sys
import os


ec2 = boto3.client('ec2')
ec2_res = boto3.resource('ec2')

ssh_client = paramiko.client.SSHClient()

instance = None
###SSH provision function

def ssh_provision(username_,hostname_):

    key_file = open('rudskoy_aws_key','r')
    pk = paramiko.RSAKey.from_private_key(key_file)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())



    for x in range(10):
        try:
            ssh_client.connect(hostname_, username=username_, pkey=pk)

        except Exception, e:
            time.sleep(5)

    ssh_client.exec_command("sudo mkfs.ext4 /dev/xvdy")
    ssh_client.exec_command("sudo mkdir /var/www && sudo mount /dev/xvdy /var/www")
    print("Magnetic volume is mounted")
    ssh_client.exec_command("sudo yum install git gcc python-pip -y")
    time.sleep(20)
    ssh_client.exec_command("sudo pip install psutil")
    time.sleep(5)
    ssh_client.exec_command("cd /var/www && sudo git clone https://github.com/krudskoy/opstask")
    print("Repository is cloned")
    time.sleep(20)
    ssh_client.exec_command("cd /var/www/opstask && python git_checker.py &> /dev/null &")
    print("Git-checker is running")

    ssh_client.close()
    key_file.close()

def create_instance(a_zone = os.environ['AWS_DEFAULT_REGION'] + 'a'):
    ##Create EC2 instance
    instances=ec2_res.create_instances(
        ImageId='ami-04681a1dbd79675a5',
        MinCount=1,
        MaxCount=1,
        KeyName="Rudskoy_Kostya",
        InstanceType="t2.micro",
        SecurityGroupIds=[security_group_id],
        Placement={
            'AvailabilityZone': a_zone
            }
    )

    global instance
    instance = instances[0]
    ##EC2 status check
    instance.wait_until_running()
    print("EC2 instance is created")
    ##Create ec2 tag
    ec2_res.create_tags(Resources=[instance.id], Tags=[{'Key':'Name', 'Value':'Rudskoy_Kostya'}])


def create_aws_key():
    response = ec2.create_key_pair(KeyName='Rudskoy_Kostya')
    key=response['KeyMaterial']
    try:
        os.remove("./rudskoy_aws_key")
    except: print('key file not present locally')
    print("Keypair is removed")
    f = open("rudskoy_aws_key","w+")
    f.write(key)
    f.close()
    os.chmod("./rudskoy_aws_key", 0o400)
    return key

##Check if instance exist
check_instance= ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'Rudskoy_Kostya',
            ]
        },
        {
            'Name': 'instance-state-name',
            'Values': [
                'running',
             ]

        },

    ]
)
if not check_instance["Reservations"]:
    print("Instance is absence")

##Check KeyPair

    check_key = ec2.describe_key_pairs(
        Filters=[
            {
                'Name': 'key-name',
                'Values': [
                    'Rudskoy_Kostya',
                ]
            },
        ]
    )

    if check_key["KeyPairs"]:
       print("Keypair is already exist")
       delete_key = ec2.delete_key_pair(
       KeyName='Rudskoy_Kostya'
       )
       key=create_aws_key()
       print("New Keypair is created")
    else:
        key=create_aws_key()
        print("Keypair is created")

##Check Security Group

    check_group = ec2.describe_security_groups(
    Filters=[
            {
                'Name': 'group-name',
                'Values': [
                    'Rudskoy_Kostya',
                ]
            },
        ]
    )
    if not check_group["SecurityGroups"]:
       print("SecurityGroup is absence")

##Check VPC id
       response = ec2.describe_vpcs()
       vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

##Create security group
       try:
            response = ec2.create_security_group(GroupName='Rudskoy_Kostya',
                                                 Description='Junior_DevOps_Test',
                                                 VpcId=vpc_id)
            security_group_id = response['GroupId']

            data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': 80,
                     'ToPort': 80,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 22,
                     'ToPort': 22,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                 ])
       except ClientError as e:
            print(e)

    else:
        print("Security Group ID exist")
        for x in check_group["SecurityGroups"]:
            security_group_id = (x["GroupId"])
            print("SecurityGroup ID is fetched")


##Check if volume exist

    check_vol = ec2.describe_volumes(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'Rudskoy_Kostya',
                ]
            },
            {
                'Name': 'status',
                'Values': [
                    'available',
                ]
            },




        ]
    )

    if not check_vol["Volumes"]:

##Create ec2 instance
        create_instance()


        ## Create a volume.
        vol = ec2_res.create_volume(Size=1, AvailabilityZone=instance.placement['AvailabilityZone'], VolumeType='Magnetic')
        vol_id = vol.id
        ec2_res.create_tags(Resources=[vol_id], Tags=[{'Key':'Name', 'Value':'Rudskoy_Kostya'}])
        waiter = ec2.get_waiter('volume_available')
        waiter.wait(VolumeIds=[vol_id])
        print("Magnetic volume is created")
        instance.attach_volume(Device='/dev/sdy', InstanceId=instance.id, VolumeId=vol_id)
        print("Magnetic volume attached")
    else:
        for x in check_vol["Volumes"]:
            vol_id = x["VolumeId"]
            vol_region = x["AvailabilityZone"]
        print("Magnetic volume ID and Region fetched")
        create_instance(vol_region)
        instance.attach_volume(Device='/dev/sdy', InstanceId=instance.id, VolumeId=vol_id)
        print("Magnetic volume attached")

#######SSH Provision########
    ssh_provision('ec2-user', instance.public_dns_name)
    print("Provision is executed successfully")
    print("\n####### Credentials ########\n")
    print("Login: root\nPassword: root")
    print("EC2: " + instance.public_dns_name)


##If instance exist
else: print("Instance is already exist")
