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
    pivots = ["pokedex_number", "pokemon"]
    
    # pokemon_has_types
    pokemon = merge_and_group(pokemon, pokemon_has_types, "pokedex_number", "pokemon_id", pivots, ["pokemon"], "type_id", "type_ids")
    
    # pokemon_has_moves
    pokemon = merge_and_group(pokemon, pokemon_has_moves, "pokedex_number", "pokemon_id", pivots, ["pokemon"], "move_id", "move_ids")

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

def merge_and_group(
        dataframe: pd.DataFrame,
        relationship_dataframe: pd.DataFrame,
        left_on: str,
        right_on: str,
        groupby: list,
        drop_columns: list,
        old_column_name: str,
        new_column_name: str,
    ) -> pd.DataFrame:
    dataframe = pd.merge(dataframe, relationship_dataframe, left_on=left_on, right_on=right_on)
    # https://stackoverflow.com/questions/64235312/how-to-implodereverse-of-pandas-explode-based-on-a-column
    grouped = dataframe.groupby(groupby).agg({old_column_name: list}).reset_index()
    grouped = grouped.drop(columns=drop_columns).rename(columns={old_column_name: new_column_name})
    dataframe = pd.merge(dataframe, grouped, on=left_on).drop(columns=[right_on, old_column_name]).drop_duplicates(subset=[left_on])
    return dataframe

def get_table(table_name: str) -> pd.DataFrame:
    mysql_engine = get_mysql_connection()
    return pd.read_sql(f"SELECT * FROM {table_name}", mysql_engine)

mySQLtoMongoDB()