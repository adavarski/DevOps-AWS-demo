### AWS docker+ansible Provisioner/Decommissioner

Provisions AWS services/resources: S3 bucket, Postgres RDS, DynamoDB table, etc. .

#### Provisioning services/resources

```sh

make build-provisioner

# Fill in the AWS credentials and region e.g. us-east-1
# The credentials should be for the "saas-provisioner" user
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_REGION="us-east-2"

make provision-resources
```

#### Decommissioning servcies/resources

```sh

make build-provisioner

# Fill in the AWS credentials and region e.g. us-east-1
# The credentials should be for the "saas-provisioner" user
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_REGION="us-east-2"

make decommission-resources
```
