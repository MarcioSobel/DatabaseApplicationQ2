from pandas import DataFrame

def pokemon(pokemon: DataFrame) -> DataFrame:
    """
    All this function does is drop columns
    that won't be used and rename columns so they fit in
    the database schema.
    """
    return pokemon.drop(columns=[
        # pokemon.csv
        "id",
        "ability1",
        "ability2",
        "abilityH",
        "forme",
        "type1",
        "type2",
        "weight",
        "height",
        "dex1",
        "dex2",
        "percent-male",
        "percent-female",
        "egg-group1",
        "egg-group2",
        "pre-evolution",

        # pokedex.csv
        "Id",
        "Name",
        "Type 1",
        "Type 2",
        "Abilities",
        "Category",
        "Height (ft)",
        "Weight (lbs)",
        "Egg Steps",
        "Exp Group",
        "Total",
        "HP",
        "Attack",
        "Defense",
        "Sp. Attack",
        "Sp. Defense",
        "Speed",
        "Moves",

        # poki_descs.csv
        "name"
    ]).rename(columns={
        "ndex": "pokedex_number",
        "species": "pokemon",
        "spattack": "special_attack",
        "spdefense": "special_defense",
        "class": "category",
        "Height (m)": "height",
        "Weight (kg)": "weight",
        "Capture Rate": "capture_rate",
        "desc": "description"
    }).drop_duplicates(subset=["pokedex_number"]).dropna(subset=["pokedex_number"])

def abilities(abilities: DataFrame) -> DataFrame:
    return abilities.rename(columns={
        "ability_id": "id",
    })

def types(types: DataFrame) -> DataFrame:
    return types.rename(columns={
        "type_id": "id",
    })

def moves(moves: DataFrame) -> DataFrame:
    return moves.drop(columns=[
        "category",
        "z-effect",
        "priority",
        "crit"
    ]).rename(columns={
        "move_id": "id",
        "pp": "power_points"
    })

def type_effectiveness(type_effectiveness: DataFrame) -> DataFrame:
    return type_effectiveness.rename(columns={
        "defense-type1": "defending_type_id",
        "defense-type2": "defending_type2_id"
    })

def addTypeFK(moves: DataFrame, types: DataFrame) -> DataFrame:
    type_to_id = types.set_index("type")["id"].to_dict() # { type: type_id }
    moves["type_id"] = moves["type"].map(type_to_id)
    return moves.drop(columns=["type"])