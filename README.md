## IaC & CI/CD tools used for this demo: Terraform, Jenkins, Docker, Git/GitHub 

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


### Note: [Create/Destroy AWS resources with Ansible:Simple Tasks->Manual and CI/CD:Ansible Tower(AWX)](https://github.com/adavarski/DevOps-AWS-demo/tree/main/ansible)

