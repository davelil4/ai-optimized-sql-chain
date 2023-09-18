import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
conn = psycopg2.connect(
    host="localhost",
    database="Adventureworks",
    user=os.environ['PG_USER'],
    password=os.environ['PG_PASS'])

def query(SQL):
    
    cur = None
    answer = None
    try:
        cur = conn.cursor()
        
        cur.execute(SQL)
        
        answer = cur.fetchall()
        
        cur.close()
    except:
        print("Failed to execute command")
    finally:
        if cur is not None:
            cur.close()
            print('Cursor connection closed.')
        
    if answer is not None:
        return answer
    return ""
