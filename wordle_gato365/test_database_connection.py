import MySQLdb
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'localhost')
db_port = int(os.getenv('DB_PORT', 3306))


connection = None

try:
    # Establish a connection to the database
    connection = MySQLdb.connect(
        host=db_host,
        user=db_user,
        passwd=db_password,
        db=db_name,
        port=db_port
    )
    print("Connection to the database was successful!")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # Execute a simple query to verify the connection
    cursor.execute("SELECT DATABASE();")
    result = cursor.fetchone()
    print(f"Connected to database: {result[0]}")

except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")

finally:
    if connection:
        connection.close()
        print("Connection closed.")