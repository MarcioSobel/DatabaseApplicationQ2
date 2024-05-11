from sqlalchemy import create_engine, Engine

def getEngine() -> Engine:
    return create_engine("mysql+pymysql://root:root@localhost:3306/pokemon")