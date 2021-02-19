### AWS docker+ansible Provisioner/Decommissioner

Provisions AWS services/resources: S3 bucket, Postgres RDS, DynamoDB table, etc. .

#### Provisioning services/resources

```sh

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
$ make build-provisioner
Sending build context to Docker daemon  121.3kB
Step 1/6 : FROM alpine:3.12
3.12: Pulling from library/alpine
801bfaa63ef2: Pull complete 
Digest: sha256:3c7497bf0c7af93428242d6176e8f7905f2201d8fc5861f45be7a346b5f23436
Status: Downloaded newer image for alpine:3.12
 ---> 389fef711851
Step 2/6 : ENV ANSIBLE_HOSTS=/ansible/hosts
 ---> Running in 016897865de0
Removing intermediate container 016897865de0
 ---> 8236a6aea9e0
Step 3/6 : RUN apk --update add py-pip ansible bash ca-certificates  && pip install --upgrade pip boto boto3  && update-ca-certificates 2&>1 > /dev/null
 ---> Running in ffa39837438f
fetch http://dl-cdn.alpinelinux.org/alpine/v3.12/main/x86_64/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.12/community/x86_64/APKINDEX.tar.gz
(1/52) Installing libbz2 (1.0.8-r1)
(2/52) Installing expat (2.2.9-r1)
(3/52) Installing libffi (3.3-r2)
(4/52) Installing gdbm (1.13-r1)
(5/52) Installing xz-libs (5.2.5-r0)
(6/52) Installing ncurses-terminfo-base (6.2_p20200523-r0)
(7/52) Installing ncurses-libs (6.2_p20200523-r0)
(8/52) Installing readline (8.0.4-r0)
(9/52) Installing sqlite-libs (3.32.1-r0)
(10/52) Installing python3 (3.8.5-r0)
(11/52) Installing yaml (0.2.4-r1)
(12/52) Installing py3-yaml (5.3.1-r1)
(13/52) Installing py3-asn1 (0.4.7-r2)
(14/52) Installing py3-cparser (2.20-r0)
(15/52) Installing py3-cffi (1.14.0-r2)
(16/52) Installing py3-idna (2.9-r0)
(17/52) Installing py3-asn1crypto (1.3.0-r0)
(18/52) Installing py3-six (1.15.0-r0)
(19/52) Installing py3-cryptography (2.9.2-r0)
(20/52) Installing py3-bcrypt (3.1.7-r2)
(21/52) Installing py3-pynacl (1.4.0-r0)
(22/52) Installing py3-paramiko (2.7.1-r0)
(23/52) Installing py3-markupsafe (1.1.1-r3)
(24/52) Installing py3-jinja2 (2.11.2-r0)
(25/52) Installing py3-pycryptodome (3.9.7-r0)
(26/52) Installing ansible (2.9.14-r0)
(27/52) Installing bash (5.0.17-r0)
Executing bash-5.0.17-r0.post-install
(28/52) Installing ca-certificates (20191127-r4)
(29/52) Installing py3-appdirs (1.4.4-r1)
(30/52) Installing py3-ordered-set (4.0.1-r0)
(31/52) Installing py3-parsing (2.4.7-r0)
(32/52) Installing py3-packaging (20.4-r0)
(33/52) Installing py3-setuptools (47.0.0-r0)
(34/52) Installing py3-chardet (3.0.4-r4)
(35/52) Installing py3-certifi (2020.4.5.1-r0)
(36/52) Installing py3-urllib3 (1.25.9-r0)
(37/52) Installing py3-requests (2.23.0-r0)
(38/52) Installing py3-msgpack (1.0.0-r0)
(39/52) Installing py3-lockfile (0.12.2-r3)
(40/52) Installing py3-cachecontrol (0.12.6-r0)
(41/52) Installing py3-colorama (0.4.3-r0)
(42/52) Installing py3-distlib (0.3.0-r0)
(43/52) Installing py3-distro (1.5.0-r1)
(44/52) Installing py3-webencodings (0.5.1-r3)
(45/52) Installing py3-html5lib (1.0.1-r4)
(46/52) Installing py3-pytoml (0.1.21-r0)
(47/52) Installing py3-pep517 (0.8.2-r0)
(48/52) Installing py3-progress (1.5-r0)
(49/52) Installing py3-toml (0.10.1-r0)
(50/52) Installing py3-retrying (1.3.3-r0)
(51/52) Installing py3-contextlib2 (0.6.0-r0)
(52/52) Installing py3-pip (20.1.1-r0)
Executing busybox-1.31.1-r19.trigger
Executing ca-certificates-20191127-r4.trigger
OK: 239 MiB in 66 packages
Collecting pip
  Downloading pip-21.0.1-py3-none-any.whl (1.5 MB)
Collecting boto
  Downloading boto-2.49.0-py2.py3-none-any.whl (1.4 MB)
Collecting boto3
  Downloading boto3-1.17.11-py2.py3-none-any.whl (130 kB)
Collecting jmespath<1.0.0,>=0.7.1
  Downloading jmespath-0.10.0-py2.py3-none-any.whl (24 kB)
Collecting botocore<1.21.0,>=1.20.11
  Downloading botocore-1.20.11-py2.py3-none-any.whl (7.2 MB)
Collecting s3transfer<0.4.0,>=0.3.0
  Downloading s3transfer-0.3.4-py2.py3-none-any.whl (69 kB)
Collecting python-dateutil<3.0.0,>=2.1
  Downloading python_dateutil-2.8.1-py2.py3-none-any.whl (227 kB)
Requirement already satisfied, skipping upgrade: urllib3<1.27,>=1.25.4 in /usr/lib/python3.8/site-packages (from botocore<1.21.0,>=1.20.11->boto3) (1.25.9)
Requirement already satisfied, skipping upgrade: six>=1.5 in /usr/lib/python3.8/site-packages (from python-dateutil<3.0.0,>=2.1->botocore<1.21.0,>=1.20.11->boto3) (1.15.0)
Installing collected packages: pip, boto, jmespath, python-dateutil, botocore, s3transfer, boto3
  Attempting uninstall: pip
    Found existing installation: pip 20.1.1
    Uninstalling pip-20.1.1:
      Successfully uninstalled pip-20.1.1
Successfully installed boto-2.49.0 boto3-1.17.11 botocore-1.20.11 jmespath-0.10.0 pip-21.0.1 python-dateutil-2.8.1 s3transfer-0.3.4
Removing intermediate container ffa39837438f
 ---> f355233d14dd
Step 4/6 : COPY cloudformation /cloudformation
 ---> ca4dd52e7867
Step 5/6 : COPY ansible /ansible
 ---> 81473dafd16a
Step 6/6 : COPY sh/* /usr/local/bin/
 ---> 8225897d05f4
Successfully built 8225897d05f4
Successfully tagged aws-ansible:local


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
