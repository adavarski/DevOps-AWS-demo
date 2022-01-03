## IaC & CI/CD tools used for this demo: Terraform, Jenkins, Docker, Git/GitHub, Ansible/AnsibleTower(AWX)

Pre: Register a free AWS account (the demo will fit into the 12 month free tier).

Simple Tasks:

- Create an EC2, and install Jenkins (also docker, awscli, terraform, etc.) on it (Terraform & J.Pipeline)
- Create a Container Registry to hold container image (Terraform & J.Pipeline)
- Create a PostgreSQL RDS instance. Connection credentials stored in AWS SSM Parameter Store (Terraform & J.Pipeline)
- Create a Docker image which contain Python application as a starting point which connects to the RDS instance and print out: RDS version & Connection properties.  Build a Docker image and upload it to the Registry (Terraform & J.Pipeline)
- Create an S3 bucket, which is public to the internet, and capable of static web hosting, uploads a static html to the S3 bucket (Terraform & J.Pipeline)

Note: All resource creation automatized with Terraform & Jenkins pipelines. 

## 1.Jenkins local instance (home laptop)

### Setup CI/CD Jenkins local environment:

```
./setup-environment.sh
```
Create J.pub/private keys: 

```
su - jenkins
ssh-keygen
```

Unlock Jenkins, Create admin/demo user, Install Sugested plugins + Docker + Docker pipelines + CloudBees AWS Credentials, Configure J.Credentials for Github (ID:devops) and DockerHub (ID: docker-hub-credentials) and AWS (ID: AWS-demo). 

Note: Add global credentials "ID: devops" with "SSH Username with private key" using J.id_rsa private key and using J.plugin "CloudBees AWS Credentials" add "AWS Credentials" (ID: AWS-demo; aws_access_key_id & aws_secret_access_key)

Setup github account (SSH keys) --> Add J.id_rsa.pub key.

### Create J.pipelines

#### Jenkinsfile-S3-website-static

Jenkinsfile-s3-web pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/S3-web/Jenkinsfile-s3-web

parameters: CREATE, UPLOAD, DESTROY

Note: Create an S3 bucket (CREATE J.pipeline parameter), which is public to the internet, and capable of static web hosting. With parameter UPLOAD: uploads a static html file to the previously created S3 bucket.

Example J.pipeline outputs:

https://github.com/adavarski/DevOps-AWS-demo/blob/main/S3-web/J-console-output/consoleText-S3-static-web-site-CREATE

https://github.com/adavarski/DevOps-AWS-demo/blob/main/S3-web/J-console-output/consoleText-S3-static-web-site-UPLOAD

https://github.com/adavarski/DevOps-AWS-demo/blob/main/S3-web/J-console-output/consoleText-S3-static-web-site-DESTROY

#### Jenkinsfile-RDS (PostgreSQL RDS)

Note: Connection credentials stored in AWS SSM ParameterStore

Jenkinsfile-RDS pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/RDS/Jenkinsfile-RDS

parameters: CREATE, DESTROY

Example J.pipeline outputs:

https://github.com/adavarski/DevOps-AWS-demo/blob/main/RDS/J-console-output/consoleText-RDS-CREATE

https://github.com/adavarski/DevOps-AWS-demo/blob/main/RDS/J-console-output/consoleText-RDS-DESTROY


#### Jenkinsfile-ECR

Jenkinsfile-ECR pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/ECR/Jenkinsfile-ECR

parameters: CREATE, DESTROY

Example J.pipeline outputs:

https://github.com/adavarski/DevOps-AWS-demo/blob/main/ECR/J-console-output/consoleText-ECR-CREATE

https://github.com/adavarski/DevOps-AWS-demo/blob/main/ECR/J-console-output/consoleText-ECR-DESTROY


#### Jenkinsfile-Docker

Jenkinsfile-docker-build-push pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/Py-Docker/Jenkinsfile-docker-py-app

Example J.pipeline output:

https://github.com/adavarski/DevOps-AWS-demo/blob/main/Py-Docker/J-console-output/consoleText-docker-py-app-build-push


#### Jenkins AWS EC2

Create "demo" AWS keypair 

Jenkinsfile-EC2 pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/Jenkins-EC2/Jenkinsfile-EC2

parameters: CREATE, DESTROY

Example J.pipeline outputs:

https://github.com/adavarski/DevOps-AWS-demo/blob/main/Jenkins-EC2/J-console-output/consoleText-CREATE-J.EC2-VM

https://github.com/adavarski/DevOps-AWS-demo/blob/main/Jenkins-EC2/J-console-output/consoleText-DESTROY-J.EC2-VM

## 2.Jenkins instance @ AWS EC2 VM 

 Pre: Using J.pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/Jenkins-EC2/Jenkinsfile-EC2 ---> Build with Parameters: CREATE 
 
 Note: All needed software is installed into EC2 VM via cloud-init and template https://github.com/adavarski/DevOps-AWS-demo/blob/main/Jenkins-EC2/user-data.tpl during `terraform apply`.
 
 Example output: https://github.com/adavarski/DevOps-AWS-demo/blob/main/Jenkins-EC2/J-console-output/consoleText-CREATE-J.EC2-VM
 
 Note: IAM EC2 Roles are the recommended way to grant your application access to AWS services. As an example, let us assume we had a web app running on our web server EC2 instance and it needs to be able to upload assets to S3. A quick way of satisfying that requirement would be to create a set of IAM access keys and
hardcode those into the application or its configuration. This however means that from that moment on it might not be very easy to update those keys unless we perform an app/config deployment. Furthermore, we might for one reason or another end up re-using the same set of keys with other applications. The security implications are evident: reusing keys increases our exposure if those get compromised and having them hardcoded greatly increases our reaction time (it takes more effort to rotate such keys). An alternative to the preceding method would be to use Roles. We would create an EC2 Role, grant it write access to the S3 bucket and assign it to the web server EC2 instance. Once the instance has booted, it is given temporary credentials which can be found in its metadata and which get changed at regular intervals. We can now instruct our web app to retrieve the current set of credentials from the instance metadata and use those to carry out
the S3 operations. If we were to use the AWS CLI on that instance, we would notice that it fetches the said metadata credentials by default. Roles can be associated with instances only at launch time, so it is a good habit to assign one to all your hosts even if they do not need it right away.
Roles can be used to assume other roles, making it possible for your instances to temporarily escalate their privileges by assuming a different role within your account or even across AWS accounts (ref: http://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html ). Example: 

Note Example: 
```
resource "aws_iam_role" "jenkins" {
    name = "jenkins"
    path = "/"
    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "jenkins" {
    name = "jenkins"
    role = "${aws_iam_role.jenkins.id}"
    policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
       {
            "Effect": "Allow",
            "Action": [
                "codecommit:Get*",
                "codecommit:GitPull",
                "codecommit:List*"
            ],
            "Resource": "*"
       },
       {
            "Effect": "Allow",
            "NotAction": [
                "s3:DeleteBucket"
            ],
            "Resource": "*"
        }
    ]
}
EOF
}

resource "aws_iam_instance_profile" "jenkins" {
    name = "jenkins"
    roles = ["${aws_iam_role.jenkins.name}"]
}

resource "aws_instance" "jenkins" {
    ami = "${var.jenkins-ami-id}"
    instance_type = "${var.jenkins-instance-type}"
    key_name = "${var.jenkins-key-name}"
    vpc_security_group_ids = ["${aws_security_group.jenkins.id}"]
    iam_instance_profile = "${aws_iam_instance_profile.jenkins.id}"
    subnet_id = "${aws_subnet.public-1.id}"
    tags { Name = "jenkins" }
    user_data = <<EOF
#!/bin/bash
set -euf -o pipefail
exec 1> >(logger -s -t $(basename $0)) 2>&1
# Install Git and set CodeComit connection settings
# (required for access via IAM roles)
yum -y install git
git config --system credential.helper '!aws codecommit credential-helper $@'
git config --system credential.UseHttpPath true
# Clone the Ansible repository
git clone https://git-codecommit.us-east-1.amazonaws.com/v1/repos/ansible /srv/ansible; chmod 700 /srv/ansible
# Install Ansible
...
### Configure ansible

...
### Run ansible-playbook (local)
salt-call state.apply
EOF

    lifecycle { create_before_destroy = true }
}
 
```
$ aws ec2 describe-instances   --filter 'Name=instance-state-name,Values=running' |   jq -r '.Reservations[].Instances[] | [.InstanceId, .PublicDnsName, .Tags[].Value] | @json'
["i-02015fceae96e0349","ec2-13-59-245-11.us-east-2.compute.amazonaws.com","Instance for DevOps demo"]
$ chmod 600 ../demo.pem
$ ssh -i ../demo.pem ubuntu@ec2-13-59-245-11.us-east-2.compute.amazonaws.com
$ sudo cat /var/lib/jenkins/secrets/initialAdminPassword
$ su - jenkins
$ ssh-keygen 
```

Setup Jenkins the same way as Jenkins local (home laptop J.instance)

Unlock Jenkins, Create admin/demo user, Install Sugested plugins + Docker + Docker pipelines + CloudBees AWS Credentials, Configure J.Credentials for Github (ID:devops) and DockerHub (ID: docker-hub-credentials) and AWS (ID: AWS-demo). 

Note: Add global credentials "ID: devops" with "SSH Username with private key" using J.id_rsa private key and using J.plugin "CloudBees AWS Credentials" add "AWS Credentials" (ID: AWS-demo; aws_access_key_id & aws_secret_access_key)

Setup github account (SSH keys) --> Add J.id_rsa.pub key.

Create J.pipelines (@ Jenkins AWS EC2 VM):


#### Jenkinsfile-RDS pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/RDS/Jenkinsfile-RDS

#### Jenkinsfile-ECR pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/ECR/Jenkinsfile-ECR

#### Jenkinsfile-docker-build-push pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/Py-Docker/Jenkinsfile-docker-py-app

#### Jenkinsfile-s3-website-static pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/S3-web/Jenkinsfile-s3-web


## 3.Docker + Ansible (using docker+ansible for CI/CD pipelines) 
### AWS docker+ansible Provisioner/Decommissioner

Provisions AWS services/resources: S3 bucket, Postgres RDS, DynamoDB table, etc. .

#### Provisioning services/resources

```sh
cd docker-ansible
make build-provisioner

# Fill in the AWS credentials and region e.g. us-east-2
# The credentials should be for the "saas-provisioner" user (or user with enough rights/permissions)
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_REGION="us-east-2"

make provision-resources
```

Example Output:
```
$ make provision-resources
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] *********************************************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************************************
ok: [localhost]

TASK [Create Free Tier Amazon Bucket] ************************************************************************************************************************************************************
changed: [localhost]

TASK [Create Free Tier Amazon RDS PostgreSQL] ****************************************************************************************************************************************************
[WARNING]: Module did not set no_log for force_update_password
changed: [localhost]

TASK [Create Dynamo DB table] ********************************************************************************************************************************************************************
changed: [localhost]

PLAY RECAP ***************************************************************************************************************************************************************************************
localhost                  : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

#### Decommissioning servcies/resources

```sh
cd docker-ansible
make build-provisioner

# Fill in the AWS credentials and region e.g. us-east-2
# The credentials should be for the "saas-provisioner" user (or user with enough rights/permissions)
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_REGION="us-east-2"

make decommission-resources
```

Example output:
```
$ make decommission-resources
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] *********************************************************************************************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************************************************************************************
ok: [localhost]

TASK [Destroy Free Tier Amazon Bucket] ***********************************************************************************************************************************************************
changed: [localhost]

TASK [Destroy Free Tier Amazon RDS PostgreSQL] ***************************************************************************************************************************************************
[WARNING]: Module did not set no_log for force_update_password
changed: [localhost]

TASK [Destroy Dynamo DB table] *******************************************************************************************************************************************************************
changed: [localhost]

PLAY RECAP ***************************************************************************************************************************************************************************************
localhost                  : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

```

Check services/resources:
```
$ aws s3api list-buckets --query "Buckets[].Name"
$ aws rds describe-db-instances
$ aws dynamodb list-tables
```

## 4.Ansible -> Manual & Ansible Tower(AWX) CI/CD

[Create/Destroy AWS resources with Ansible:Simple Tasks->Manual and CI/CD:Ansible Tower(AWX)](https://github.com/adavarski/DevOps-AWS-demo/tree/main/ansible)

## 5. k8s provisioning on AWS with Terrafrom (KOPS & AWS EKS managed k8s) -> Ref: https://github.com/adavarski/aws-k8s-demo & https://github.com/adavarski/aws-eks-production

## 6. Provisioning development Amazon EKS clusters using Cloudformation -> Ref: https://github.com/adavarski/aws-eks-cloudformation-demo

