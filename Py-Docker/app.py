import psycopg2
import sys
import boto3

ENDPOINT="demodb-postgres.ci57iu38pu8h.us-east-2.rds.amazonaws.com"
PORT="5432"
USR="postgres"
REGION="us-east-2"
DBNAME="demodb"
PASS="Kr0k0dil!"


try:
    conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASS)
    cur = conn.cursor()
    cur.execute("""SELECT version()""")
    query_results = cur.fetchall()
    print(query_results)
    print(conn)
except Exception as e:
    print("Database connection failed due to {}".format(e))   
