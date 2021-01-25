
#### Simple Tasks(manual):

- Free Tier Amazon S3 bucket
- Free Tier Amazon RDS PostgreSQL
- DynamoDB table in Free Tier Amazon DynamoDB:
CREATE TABLE Music ( Artist VARCHAR(20) NOT NULL, SongTitle VARCHAR(30) NOT NULL, AlbumTitle VARCHAR(25), Year INT, Price FLOAT, Genre VARCHAR(10), Tags TEXT, PRIMARY KEY(Artist, SongTitle) );
- Create an AWS Lambda function using Python runtime to ping google.com once every 10 secs for 5 minutes continuously.



1.Install ansible 
```
sudo apt-add-repository ppa:ansible/ansible
sudo apt update
sudo apt install ansible
```

2.Install boto3 via pip3 and configure aws cli credentials (aws configure) or edit playbooks:

```
- hosts: localhost
  environment:
    AWS_ACCESS_KEY_ID: "{{ aws_access_key }}"
    AWS_SECRET_ACCESS_KEY: "{{ aws_secret_key }}"
    AWS_REGION: "{{ aws_region }}"
```
Note: Better use ansible vault for AWS credentials/config.

3.Create new IAM role (AWS console->IAM:Roles): Lambda_Full with Policy: AWSLambda_FullAccess and get role ARN (update create_resources.yml & delete-resources.yml with role ARN)

```
$ aws iam get-role --role-name Lambda_Full
{
    "Role": {
        "Path": "/",
        "RoleName": "Lambda_Full",
        "RoleId": "AROATF2CKGXNU4IKJCM54",
        "Arn": "arn:aws:iam::218645542363:role/Lambda_Full",
        "CreateDate": "2021-01-21T11:57:06Z",
        "AssumeRolePolicyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        },
        "Description": "Allows Lambda functions to call AWS services on your behalf.",
        "MaxSessionDuration": 3600,
        "RoleLastUsed": {
            "LastUsedDate": "2021-01-21T12:37:37Z",
            "Region": "us-east-2"
        }
    }
}
```

4.Create AWS resources:
```
ansible-playbook create_resources.yml
```
Example output:

```
$ ansible-playbook create_resources.yml 
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] ************************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************
ok: [localhost]

TASK [Create Free Tier Amazon Bucket] ***************************************************************************************************************************************
changed: [localhost]

TASK [Create Free Tier Amazon RDS PostgreSQL] *******************************************************************************************************************************
[WARNING]: Module did not set no_log for force_update_password
changed: [localhost]

TASK [Create Dynamo DB table] ***********************************************************************************************************************************************
changed: [localhost]

TASK [Create lambda in AWS] *************************************************************************************************************************************************
changed: [localhost]

PLAY RECAP ******************************************************************************************************************************************************************
localhost                  : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
5.Check AWS resources:
```
aws s3 cp ./ping.py s3://s3bucket-ansible/
aws s3 ls s3://s3bucket-ansible/
aws s3 rm s3://s3bucket-ansible/ --recursive
aws dynamodb list-tables
aws rds describe-db-instances --db-instance-identifier ansible-demo-postgres-db-instance
aws lambda list-functions --max-items 10
aws lambda invoke --function-name Ping out --log-type Tail --query 'LogResult' --output text |  base64 -d
```
Example output:
```
$ aws s3 cp ./ping.py s3://s3bucket-ansible/
upload: ./ping.py to s3://s3bucket-ansible/ping.py                  
$ aws s3 ls s3://s3bucket-ansible/
2021-01-21 14:31:19        736 ping.py
$ aws s3 rm s3://s3bucket-ansible/ --recursive
delete: s3://s3bucket-ansible/ping.py

$ aws rds describe-db-instances --db-instance-identifier ansible-demo-postgres-db-instance
{
    "DBInstances": [
        {
            "DBInstanceIdentifier": "ansible-demo-postgres-db-instance",
            "DBInstanceClass": "db.t2.micro",
            "Engine": "postgres",
            "DBInstanceStatus": "available",
            "MasterUsername": "postgres",
            "Endpoint": {
                "Address": "ansible-demo-postgres-db-instance.ci57iu38pu8h.us-east-2.rds.amazonaws.com",
                "Port": 5432,
                "HostedZoneId": "Z2XHWR1WZ565X2"
            },
            "AllocatedStorage": 10,
            "InstanceCreateTime": "2021-01-21T12:23:18.554Z",
            "PreferredBackupWindow": "05:44-06:14",
            "BackupRetentionPeriod": 1,
            "DBSecurityGroups": [],
            "VpcSecurityGroups": [
                {
                    "VpcSecurityGroupId": "sg-0fc3eb7f",
                    "Status": "active"
                }
            ],
            "DBParameterGroups": [
                {
                    "DBParameterGroupName": "default.postgres12",
                    "ParameterApplyStatus": "in-sync"
                }
            ],
            "AvailabilityZone": "us-east-2a",
            "DBSubnetGroup": {
                "DBSubnetGroupName": "default",
                "DBSubnetGroupDescription": "default",
                "VpcId": "vpc-9568d3fe",
                "SubnetGroupStatus": "Complete",
                "Subnets": [
                    {
                        "SubnetIdentifier": "subnet-81a7befb",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-2b"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-4526852e",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-2a"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    },
                    {
                        "SubnetIdentifier": "subnet-ab6020e7",
                        "SubnetAvailabilityZone": {
                            "Name": "us-east-2c"
                        },
                        "SubnetOutpost": {},
                        "SubnetStatus": "Active"
                    }
                ]
            },
            "PreferredMaintenanceWindow": "sat:10:30-sat:11:00",
            "PendingModifiedValues": {},
            "LatestRestorableTime": "2021-01-21T12:24:30.967Z",
            "MultiAZ": false,
            "EngineVersion": "12.4",
            "AutoMinorVersionUpgrade": true,
            "ReadReplicaDBInstanceIdentifiers": [],
            "LicenseModel": "postgresql-license",
            "OptionGroupMemberships": [
                {
                    "OptionGroupName": "default:postgres-12",
                    "Status": "in-sync"
                }
            ],
            "PubliclyAccessible": true,
            "StorageType": "gp2",
            "DbInstancePort": 0,
            "StorageEncrypted": false,
            "DbiResourceId": "db-JVFTROWXWGLMXCC5W3XSDM3GYE",
            "CACertificateIdentifier": "rds-ca-2019",
            "DomainMemberships": [],
            "CopyTagsToSnapshot": false,
            "MonitoringInterval": 0,
            "DBInstanceArn": "arn:aws:rds:us-east-2:218645542363:db:ansible-demo-postgres-db-instance",
            "IAMDatabaseAuthenticationEnabled": false,
            "PerformanceInsightsEnabled": false,
            "DeletionProtection": false,
            "AssociatedRoles": [],
            "TagList": [],
            "CustomerOwnedIpEnabled": false
        }
    ]
}

$ aws dynamodb list-tables
{
    "TableNames": [
        "Music"
    ]
}


$ aws lambda list-functions --max-items 10
{
    "Functions": [
        {
            "FunctionName": "Ping",
            "FunctionArn": "arn:aws:lambda:us-east-2:218645542363:function:Ping",
            "Runtime": "python3.6",
            "Role": "arn:aws:iam::218645542363:role/Lambda_Full",
            "Handler": "ping.lambda_handler",
            "CodeSize": 479,
            "Description": "",
            "Timeout": 350,
            "MemorySize": 128,
            "LastModified": "2021-01-21T12:27:22.535+0000",
            "CodeSha256": "xj1W3SDvSHVM6Qh6h9dc4Sftv0uxf+qS5LTKuDht/e0=",
            "Version": "$LATEST",
            "TracingConfig": {
                "Mode": "PassThrough"
            },
            "RevisionId": "80aa82e7-6394-4963-9833-9cb4130942f8",
            "PackageType": "Zip"
        }
    ]
}

$ aws lambda invoke --function-name Ping out --log-type Tail --query 'LogResult' --output text |  base64 -d
START RequestId: 8d09f5fa-00a2-45bf-8c0f-1f7b876bef2b Version: $LATEST
Google.com unreacble
Google.com unreacble
Google.com unreacble
END RequestId: 8d09f5fa-00a2-45bf-8c0f-1f7b876bef2b
REPORT RequestId: 8d09f5fa-00a2-45bf-8c0f-1f7b876bef2b	Duration: 30111.46 ms	Billed Duration: 30112 ms	Memory Size: 128 MB	Max Memory Used: 45 MB	Init Duration: 1.28 ms	

```
6.Cleaning AWS resources: 
```
ansible-playbook destroy_resources.yml
```
Example output:
```
$ ansible-playbook destroy_resources.yml 
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] ************************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************
ok: [localhost]

TASK [Destroy Free Tier Amazon Bucket] ***************************************************************************************************************************************
changed: [localhost]

TASK [Destroy Free Tier Amazon RDS PostgreSQL] *******************************************************************************************************************************
[WARNING]: Module did not set no_log for force_update_password
changed: [localhost]

TASK [Destroy Dynamo DB table] ***********************************************************************************************************************************************
changed: [localhost]

TASK [Destroy lambda in AWS] *************************************************************************************************************************************************
changed: [localhost]

PLAY RECAP ******************************************************************************************************************************************************************
localhost                  : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```
7.Check AWS resources

Example output:

```
$ aws s3api list-buckets --query "Buckets[].Name"
[]

$ aws rds describe-db-instances 
{
    "DBInstances": []
}

$ aws dynamodb list-tables
{
    "TableNames": []
}

$ aws lambda list-functions --max-items 10
{
    "Functions": []
}
```
#### Ansible Tower (AWX) CI/CD (docker-compose based install)

```
pip3 install docker-compose
git clone https://github.com/ansible/awx; cd awx/installer
#Edit inventory:  admin_password=password
mkdir ~/.awx; chown -R $USER: ~/.awx
# Run the Ansible playbook to install AWX
ansible-playbook -i inventory -e docker_registry_password=password install.yml
```

Check:

```
#Check docker containers

$ docker ps -a
CONTAINER ID        IMAGE                COMMAND                  CREATED             STATUS              PORTS                  NAMES
92953d164acd        ansible/awx:17.0.0   "/usr/bin/tini -- /u…"   2 hours ago         Up 2 hours          8052/tcp               awx_task
314b0633a4e4        ansible/awx:17.0.0   "/usr/bin/tini -- /b…"   2 hours ago         Up 2 hours          0.0.0.0:80->8052/tcp   awx_web
e795ba75ab75        postgres:12          "docker-entrypoint.s…"   2 hours ago         Up 2 hours          5432/tcp               awx_postgres
1d86f1c58351        redis                "docker-entrypoint.s…"   2 hours ago         Up 2 hours          6379/tcp               awx_redis

#Check awx_task (look for PG migration), tail the awx_task log

$ docker logs -f awx_task
```

Setup Ansible Tower (AWX) with Your Ansible Project and templates.

Once Ansible AWX (Tower) is up and running first few things that we need to configure are:

- Set Up Credentials:

AWS Credentials to sync with AWS Services (AWS-credentials; Credential Type: Amazon Web Services)
GitHub (or Bitbucket, etc.) credentials to sync with our Ansible repos (Github-credentials:user&password; Credential Type:Source Control or Github Personal Access Token)
AWS Private Key File to connect to Instances (optional)

- Setup Ansible Project:

Ansible Tower needs to add templates/job to run playbooks for that we need to add our Ansible project repository in Ansible Tower.
Just like Credentials, go to Projects menu on left side.
Add new project (AWS-demo; Sync)
Fill required information to configure your project (Note here we are required to select credentials configured in the first step to add project).

- Setup Templates:

Lastly, add a template which is nothing but adding playbook as a template so that whenever you want to start/configure any AWS servcies you are only required to run this template as a job.
Just like Projects and Credentials, create a new template using left bar Menu and add a new template.
Add new template for create/destroy AWS resources using right playbooks.

Note: Make sure we add one template for each Role we have in our deployment stack create/destroy (or i.e., application, web, and database). Tower-sync utility triggers the template on the basis of Role tag configured in an instance. Make sure you tick the prompt on-launch checkbox for Inventory and extra variables section while creating Template. The reason behind this is, when tower-sync utility will trigger job it will run this template for dynamic inventory created for AWS ASG group and it will send some extra variables as a part of the trigger to identify which environment it’s running and which service its deploying.


- Lounch Templete(View Job): AWS-demo-create-resources

Check AWS resources creattion:
```
$ aws dynamodb list-tables
$ aws rds describe-db-instances --db-instance-identifier ansible-demo-postgres-db-instance
$ aws lambda list-functions --max-items 10
$ aws lambda invoke --function-name Ping out --log-type Tail --query 'LogResult' --output text |  base64 -d
$ aws s3api list-buckets --query "Buckets[].Name"
```

- Lounch Templete(View Jobs): AWS-demo-delete-resources

Check AWS resources deletion:
```
$ aws dynamodb list-tables
$ aws rds describe-db-instances --db-instance-identifier ansible-demo-postgres-db-instance
$ aws lambda list-functions --max-items 10
$ aws lambda invoke --function-name Ping out --log-type Tail --query 'LogResult' --output text |  base64 -d
$ aws s3api list-buckets --query "Buckets[].Name"
```
