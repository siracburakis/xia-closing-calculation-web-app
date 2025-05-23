from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

load_dotenv()

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
server = os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
driver = "ODBC Driver 17 for SQL Server"

connection_string = (
    f"mssql+pyodbc://{username}:{password}@{server}/{database}"
    f"?driver={driver}"
)
engine = create_engine(connection_string)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Bağlantı başarılı")
            return True
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return False
    
if __name__ == "__main__":
    test_connection()