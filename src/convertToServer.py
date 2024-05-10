import pandas as pd
from sqlalchemy import create_engine, text, Engine, MetaData
from getDataFrame import *
from cleanup import *
from resetDatabase import *

def csvToSQL() -> None:
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/pokemon")

    abilities = getDataFrame("abilities.csv")
    pokemon = getDataFrame("pokemon.csv")
    pokemonWithMoves = getDataFrame("pokedex.csv")
    pokemon = pd.merge(pokemon, pokemonWithMoves, left_on="ndex", right_on="Id", how="left")

    abilities = createAutoIncrementColumn(abilities, "ability_id")

    # create relationships
    # pokemon_has_abilities
    pokemon_has_abilities = pd.DataFrame()
    abilities_list = ["ability1", "ability2", "abilityH"]

    for ability in abilities_list:
        temp = pd.merge(pokemon, abilities, left_on=ability, right_on="ability", how="left")
        temp = temp[["ndex", "ability_id"]].rename(columns={"ndex": "pokemon_id"}).dropna()
        pokemon_has_abilities = pd.concat([pokemon_has_abilities, temp])
    pokemon_has_abilities = pokemon_has_abilities.drop_duplicates()

    # pokemon_evoles_to_pokemon
    pokemon_evolves_to_pokemon = pd.DataFrame()

    name_to_id = pokemon.set_index("species")["ndex"].to_dict() # { pokemon_name: pokemon_id }
    temp = pokemon.copy()
    temp["pokemon_id"] = pokemon["pre-evolution"].map(name_to_id)

    temp = temp.dropna(subset=["pokemon_id"])
    pokemon_evolves_to_pokemon = temp[["pokemon_id", "ndex"]].rename(columns={"ndex": "evolves_to"})
    pokemon_evolves_to_pokemon = pokemon_evolves_to_pokemon.drop_duplicates()
    pokemon_evolves_to_pokemon = pokemon_evolves_to_pokemon.rename(columns={"pokemon_id": "evolves_from"})

    # cleanup
    pokemon = cleanUpPokemon(pokemon)
    abilities = cleanUpAbilities(abilities)

    # reset database (so foreign keys work)
    resetDatabase(engine)

    # send to sql
    pokemon.to_sql("pokemon", con=engine, index=False, if_exists="append")
    abilities.to_sql("abilities", con=engine, index=False, if_exists="append")
    pokemon_has_abilities.to_sql("pokemon_has_abilities", con=engine, index=False, if_exists="append")
    pokemon_evolves_to_pokemon.to_sql("pokemon_evolves_to_pokemon", con=engine, index=False, if_exists="append")

    print(f"sucessfully uploaded data to SQL server")

# for later

# relations
# pd.merge(df_1, df_2, left_on="left_id", right_on="right_id", how="left")
# df.astype(type) (str | number -> type)
# pd.concat: https://pandas.pydata.org/docs/reference/api/pandas.concat.html

# json (pokemon moves)
# json.loads (str -> dic)
# df.apply: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html