from pandas import DataFrame

def cleanUpPokemon(pokemon: DataFrame) -> DataFrame:
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
        "Moves"
    ]).rename(columns={
        "ndex": "pokedex_number",
        "species": "name",
        "spattack": "special_attack",
        "spdefense": "special_defense",
        "class": "category",
        "Height (m)": "height",
        "Weight (kg)": "weight",
        "Capture Rate": "capture_rate"
    }).drop_duplicates(subset=["pokedex_number"]).dropna(subset=["pokedex_number"])

def cleanUpAbilities(abilities: DataFrame) -> DataFrame:
    return abilities.rename(columns={
        "ability_id": "id",
        "ability": "name"
    })