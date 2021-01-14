Jenkinsfile-docker-build-push pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/Py-Docker/Jenkinsfile-docker-py-app

Check J.Pipeline Output:

https://github.com/adavarski/DevOps-AWS-demo/blob/main/Py-Docker/J-console-output/consoleText-docker-py-app-build-push

Note: Docker image which contain Python application as a starting point which connects to the RDS instance and print out: RDS version & Connection properties

Test docker image:

```
docker build -t davarski/rds-py .

$ docker run davarski/rds-py
[('PostgreSQL 11.4 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.3 20140911 (Red Hat 4.8.3-9), 64-bit',)]
<connection object at 0x7fc7943e73f0; dsn: 'user=postgres password=xxx dbname=demodb host=demodb-postgres.ci57iu38pu8h.us-east-2.rds.amazonaws.com port=5432', closed: 0>

```
Note: AWS SSM Parameter Store check 

```
$ python
Python 2.7.17 (default, Sep 30 2020, 13:38:04) 
[GCC 7.5.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import boto3
>>> session = boto3.Session(region_name='us-east-2')
>>> ssm = session.client('ssm')
>>> db = ssm.get_parameter(Name='/demodb/demo/DATABASE_URL', WithDecryption=True)
>>> print(db['Parameter']['Value'])
postgres://postgres:Kr0k0dil!@demodb-postgres.ci57iu38pu8h.us-east-2.rds.amazonaws.com:5432/demodb
>>> url=db['Parameter']['Value']
>>> url
u'postgres://postgres:Kr0k0dil!@demodb-postgres.ci57iu38pu8h.us-east-2.rds.amazonaws.com:5432/demodb'
```
```
$ aws ssm get-parameters-by-path --path /demodb/demo --recursive --with-decryption --output text --query "Parameters[].[Name,Value]"
/demodb/demo/DATABASE_URL	postgres://postgres:Kr0k0dil!@demodb-postgres.ci57iu38pu8h.us-east-2.rds.amazonaws.com:5432/demodb
```


