import psycopg2

hostname='localhost'
database='xpayback'
username='postgres'
pwd='Global12$'
port_id=5432
conn=None
cur=None
try:
    conn=psycopg2.connect(
        host=hostname,
        dbname=database,
        user=username,
        password=pwd,
        port=port_id
    )
    
    cur=conn.cursor()
    
except Exception as error:
    print(error)
