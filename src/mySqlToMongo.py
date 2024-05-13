import pandas as pd
from connections import *

def mySQLtoMongoDB():
    mongodb_client: MongoClient = get_mongodb_client()

    pokemon = get_table("pokemon")
    types = get_table("types")
    moves = get_table("moves")

    ######### CONVERT FROM DATAFRAME TO DICTS #########
    pokemon = pokemon.to_dict("records")
    types = types.to_dict("records")

    ######### SEND TO MONGODB #########
    mongodb_client.drop_database("pokemon")
    db = mongodb_client["pokemon"]
    
    db.pokemon.insert_many(pokemon)
    db.types.insert_many(types)

    print("sucessfully uploaded data to MongoDB server")

def get_table(table_name: str) -> pd.DataFrame:
    mysql_engine = get_mysql_connection()
    return pd.read_sql(f"SELECT * FROM {table_name}", mysql_engine)

mySQLtoMongoDB()