import pandas as pd
from connections import *

def mySQLtoMongoDB():
    mongodb_client: MongoClient = get_mongodb_client()

    pokemon = get_table("pokemon")
    types = get_table("types")
    moves = get_table("moves")

    pokemon_has_types = get_table("pokemon_has_types")
    pokemon_has_moves = get_table("pokemon_has_moves")

    ######### HANDLE RELATIONSHIPS #########
    # https://stackoverflow.com/questions/64235312/how-to-implodereverse-of-pandas-explode-based-on-a-column
    # pokemon_has_types
    pokemon = pd.merge(pokemon, pokemon_has_types, left_on="pokedex_number", right_on="pokemon_id")
    temp = pokemon.groupby(["pokedex_number", "pokemon"]).agg({"type_id": list}).reset_index()
    temp = temp.drop(columns=["pokemon"]).rename(columns={"type_id": "type_ids"})
    pokemon = pd.merge(pokemon, temp, on="pokedex_number").drop(columns=["pokemon_id", "type_id"]).drop_duplicates(subset=["pokedex_number"])
    
    # pokemon_has_moves
    pokemon = pd.merge(pokemon, pokemon_has_moves, left_on="pokedex_number", right_on="pokemon_id")
    temp = pokemon.groupby(["pokedex_number", "pokemon"]).agg({"move_id": list}).reset_index()
    temp = temp.drop(columns=["pokemon"]).rename(columns={"move_id": "move_ids"})
    pokemon = pd.merge(pokemon, temp, on="pokedex_number").drop(columns=["pokemon_id", "move_id"]).drop_duplicates(subset=["pokedex_number"])
    print(pokemon)

    ######### RENAME ID COLUMNS TO _ID #########
    pokemon = pokemon.rename(columns={"pokedex_number": "_id"})
    types = types.rename(columns={"id": "_id"})
    moves = moves.rename(columns={"id": "_id"})

    ######### CONVERT FROM DATAFRAME TO DICTS #########
    pokemon = pokemon.to_dict("records")
    types = types.to_dict("records")
    moves = moves.to_dict("records")

    ######### SEND TO MONGODB #########
    mongodb_client.drop_database("pokemon")
    db = mongodb_client["pokemon"]
    
    db.pokemon.insert_many(pokemon)
    db.types.insert_many(types)
    db.moves.insert_many(moves)

    print("sucessfully uploaded data to MongoDB server")

def get_table(table_name: str) -> pd.DataFrame:
    mysql_engine = get_mysql_connection()
    return pd.read_sql(f"SELECT * FROM {table_name}", mysql_engine)

mySQLtoMongoDB()