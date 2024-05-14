import pandas as pd
from connections import *

def mySQLtoMongoDB():
    pokemon = get_table("pokemon")
    types = get_table("types")
    moves = get_table("moves")
    abilities = get_table("abilities")

    pokemon_has_types = get_table("pokemon_has_types")
    pokemon_has_moves = get_table("pokemon_has_moves")
    type_effectiveness = get_table("type_effectiveness")
    pokemon_has_abilities = get_table("pokemon_has_abilities")
    pokemon_evolves_to_pokemon = get_table("pokemon_evolves_to_pokemon")

    ######### HANDLE RELATIONSHIPS #########
    pivots = ["pokedex_number", "pokemon"]
    
    # pokemon_has_types
    pokemon = merge_and_group(pokemon, pokemon_has_types, "pokedex_number", "pokemon_id", pivots, ["pokemon"], "type_id", "type_ids")
    
    # pokemon_has_moves
    pokemon = merge_and_group(pokemon, pokemon_has_moves, "pokedex_number", "pokemon_id", pivots, ["pokemon"], "move_id", "move_ids")

    # pokemon_has_abilities
    pokemon = merge_and_group(pokemon, pokemon_has_abilities, "pokedex_number", "pokemon_id", pivots, ["pokemon"], "ability_id", "ability_ids")

    # pokemon_evolves_to_pokemon
    pokemon = merge_and_group(pokemon, pokemon_evolves_to_pokemon, "pokedex_number", "evolves_from", pivots, ["pokemon"], "evolves_to")

    # type_effectiveness
    type_effectiveness = type_effectiveness_to_dict(type_effectiveness)

    ######### RENAME ID COLUMNS TO _ID #########
    pokemon = pokemon.rename(columns={"pokedex_number": "_id"})
    abilities = abilities.rename(columns={"id": "_id"})
    types = types.rename(columns={"id": "_id"})
    moves = moves.rename(columns={"id": "_id"})

    ######### CONVERT FROM DATAFRAME TO DICTS #########
    pokemon = pokemon.to_dict("records")
    types = types.to_dict("records")
    moves = moves.to_dict("records")
    abilities = abilities.to_dict("records")

    ######### SEND TO MONGODB #########
    mongodb_client = MongoClient("mongodb://root:root@localhost:27017")
    mongodb_client.drop_database("pokemon")
    db = mongodb_client["pokemon"]
    
    db.pokemon.insert_many(pokemon)
    db.types.insert_many(types)
    db.moves.insert_many(moves)
    db.abilities.insert_many(abilities)
    db.type_effectiveness.insert_many(type_effectiveness)

    print("sucessfully uploaded data to MongoDB server")

def merge_and_group(
        dataframe: pd.DataFrame,
        relationship_dataframe: pd.DataFrame,
        left_on: str,
        right_on: str,
        groupby: list,
        drop_columns: list,
        old_column_name: str,
        new_column_name: str = "",
    ) -> pd.DataFrame:
    dataframe = pd.merge(dataframe, relationship_dataframe, left_on=left_on, right_on=right_on, how="left")
    # https://stackoverflow.com/questions/64235312/how-to-implodereverse-of-pandas-explode-based-on-a-column
    grouped = dataframe.groupby(groupby).agg({old_column_name: list}).reset_index()
    grouped = grouped.drop(columns=drop_columns)
    if new_column_name:
        grouped = grouped.rename(columns={old_column_name: new_column_name})
        dataframe = pd.merge(dataframe, grouped, on=left_on).drop(columns=[right_on, old_column_name]).drop_duplicates(subset=[left_on])
    else:
        dataframe = pd.merge(dataframe, grouped, on=left_on).drop(columns=[right_on]).drop_duplicates(subset=left_on)
        dataframe = dataframe.drop(columns=[f"{old_column_name}_x"]).rename(columns={f"{old_column_name}_y": old_column_name})
    return dataframe

def type_effectiveness_to_dict(dataFrame: pd.DataFrame) -> list:
    dataFrame["defending_type_ids"] = dataFrame[['defending_type_id', 'defending_type2_id']].values.tolist()
    dataFrame["defending_type_ids"] = dataFrame["defending_type_ids"].apply(lambda x: [int(i) if i.is_integer() else i for i in x])
    dataFrame = dataFrame.drop(columns=["defending_type_id", "defending_type2_id"])
    dataFrame["against"] = dataFrame[["multiplier", "defending_type_ids"]].values.tolist()
    dataFrame = dataFrame.groupby("attacking_type_id")["against"].apply(list).reset_index()

    result = []
    for _, row in dataFrame.iterrows():
        row_doc = {}
        row_doc["type_id"] = row["attacking_type_id"]
        row_doc["against"] = []

        for item in row["against"]:
            item_doc = {}
            item_doc["type_ids"] = [x for x in item[1] if pd.notna(x)]
            item_doc["multiplier"] = item[0]

            row_doc["against"].append(item_doc)
        result.append(row_doc)
    return result

def get_table(table_name: str) -> pd.DataFrame:
    mysql_engine = get_mysql_connection()
    return pd.read_sql(f"SELECT * FROM {table_name}", mysql_engine)