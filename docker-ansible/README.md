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
