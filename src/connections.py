from pymongo import MongoClient
from sqlalchemy import create_engine, Engine

def get_mysql_connection() -> Engine:
    return create_engine("mysql+pymysql://root:root@localhost:3306/pokemon")

def get_mongodb_client() -> MongoClient:
    return MongoClient("mongodb://root:root@localhost:27017")