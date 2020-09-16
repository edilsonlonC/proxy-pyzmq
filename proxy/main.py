from dotenv import load_dotenv

load_dotenv()

import os 
from database import database

db_name = os.getenv('DB_NAME')
print(db_name)