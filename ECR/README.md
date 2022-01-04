
Jenkinsfile-ECR pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/ECR/Jenkinsfile-ECR

Build with Parameters: CREATE

Check J. Console Output: 

https://github.com/adavarski/DevOps-AWS-demo/blob/main/ECR/J-console-output/consoleText-ECR-CREATE

Check AWS ECR:

```
$ aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 218645542363.dkr.ecr.us-east-2.amazonaws.com
Login Succeeded

$ docker images|grep "davarski/rds-py"|grep latest|awk '{print $3}'
8b262e3eb0c7

$ docker tag `docker images|grep "davarski/rds-py"|grep latest|awk '{print $3}'` 218645542363.dkr.ecr.us-east-2.amazonaws.com/demo-repo:latest

$ docker push 218645542363.dkr.ecr.us-east-2.amazonaws.com/demo-repo:latest
The push refers to repository [218645542363.dkr.ecr.us-east-2.amazonaws.com/demo-repo]
ee42427cb5f8: Pushed 
79f96b805703: Pushed 
0c91787a036f: Pushed 
9895fc0ba63c: Pushed 
be483c022f0b: Pushed 
67bc8627401f: Pushed 
82d83d6c1a37: Pushed 
0b776d2c2318: Pushed 
5dacd731af1b: Pushed 
latest: digest: sha256:b3eb87a38a9f89bda06bbb1f2087cc8b4f4ed5e94b802bee173d5f256bed94b4 size: 2203

```

Note: Amazon ECR Docker Credential Helper -> REF: https://github.com/awslabs/amazon-ecr-credential-helper (The Amazon ECR Docker Credential Helper is a credential helper for the Docker daemon that makes it easier to use Amazon Elastic Container Registry.)

Example:
```
$ sudo apt update
$ sudo apt install amazon-ecr-credential-helper

$ davar@devops (K8S):~/.docker# cat config.json 
{
    "credsStore": "ecr-login"
}

$ davar@devops (K8S):~/.docker# cat ~/.aws/credentials 
[default]
aws_access_key_id = XXXXX
aws_secret_access_key = YYYYYY

[k8s]
aws_access_key_id = XXXXX
aws_secret_access_key = YYYYY

$ davar@devops (K8S):~/.docker# cat ~/.aws/config 
[profile default]
output = json
region = us-east-1

$ export AWS_PROFILE=k8

$ docker tag web-php 218645542363.dkr.ecr.eu-west-1.amazonaws.com/web-php
$ docker push 218645542363.dkr.ecr.eu-west-1.amazonaws.com/web-php
```
