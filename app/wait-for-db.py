import sys
import time
import pymysql

max_attempts = 30
attempt = 0

while attempt < max_attempts:
    try:
        connection = pymysql.connect(
            host="mysql-fastapi",
            user="root",
            password="root",
            db="fastapi_blog",
        )
        connection.close()
        print("Database is ready!")
        sys.exit(0)
    except pymysql.MySQLError as e:
        attempt += 1
        print(
            f"Attempt {attempt}/{max_attempts}: Database is not ready yet, waiting...")
        time.sleep(5)

print("Max attempts reached, exiting...")
sys.exit(1)
