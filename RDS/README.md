
Jenkinsfile-RDS pipeline: https://github.com/adavarski/DevOps-AWS-demo/blob/main/RDS/Jenkinsfile-RDS

Build with parameters: CREATE

Check J.Console Output:

https://github.com/adavarski/DevOps-AWS-demo/blob/main/RDS/J-console-output/consoleText-RDS-CREATE

Check AWS RDS (PostgreSQL):

```
$ python3
Python 3.8.5 (default, Jul 28 2020, 12:59:40) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
>>> import psycopg2
>>> import sys
>>> import boto3
>>> 
>>> ENDPOINT="demodb-postgres.ci57iu38pu8h.us-east-2.rds.amazonaws.com"
>>> PORT="5432"
>>> USR="postgres"
>>> REGION="us-east-2"
>>> DBNAME="demodb"
>>> PASS="Kr0k0dil!"
>>> 
>>> 
>>> try:
...     conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
...     cur = conn.cursor()
...     cur.execute("""SELECT version()""")
...     query_results = cur.fetchall()
...     print(query_results)
... except Exception as e:
...     print("Database connection failed due to {}".format(e))   
... 
[('PostgreSQL 11.4 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 4.8.3 20140911 (Red Hat 4.8.3-9), 64-bit',)]
>>> 
```
Check SSM Parameter Store:
```
$ aws rds describe-db-instances --db-instance-identifier demodb-postgres|grep -i address
                "Address": "demodb-postgres.ci57iu38pu8h.us-east-2.rds.amazonaws.com",

$ aws ssm get-parameters-by-path --path /demodb/demo --recursive --with-decryption --output text --query "Parameters[].[Name,Value]"
/demodb/demo/DATABASE_URL	postgres://postgres:Kr0k0dil!@demodb-postgres.ci57iu38pu8h.us-east-2.rds.amazonaws.com:5432/demodb

```
