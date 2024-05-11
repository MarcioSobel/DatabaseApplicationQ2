import pandas as pd
import cleanup
from sqlalchemy import create_engine
from getDataFrame import *
from resetDatabase import *

def csvToSQL() -> None:
    pokemon = getDataFrame("pokemon")
    abilities = getDataFrame("abilities")
    type_chart = getDataFrame("type-chart")
    types = type_chart.copy()

    pokemonWithMoves = getDataFrame("pokedex")
    pokemonDescriptions = getDataFrame("poki_descs")
    pokemon = pd.merge(pokemon, pokemonWithMoves, left_on="ndex", right_on="Id")
    pokemon = pd.merge(pokemon, pokemonDescriptions, left_on="species", right_on="name", how="left")

    abilities = createAutoIncrementColumn(abilities, "ability_id")
    
    types = pokemon[["type1"]].rename(columns={"type1": "type"}).drop_duplicates()
    types = createAutoIncrementColumn(types, "type_id")
    types_lowercase = types["type"].apply(lambda x: pd.Series(str.lower(x))).rename(columns={0: "type"})
    types_lowercase["type_id"] = types["type_id"]

    ########## RELATIONSHIPS ##########
    # pokemon_has_abilities
    pokemon_has_abilities = pd.DataFrame()
    abilities_list = ["ability1", "ability2", "abilityH"]

    for ability in abilities_list:
        temp = pd.merge(pokemon, abilities, left_on=ability, right_on="ability")
        temp = temp[["ndex", "ability_id"]].rename(columns={"ndex": "pokemon_id"}).dropna()
        pokemon_has_abilities = pd.concat([pokemon_has_abilities, temp])
    pokemon_has_abilities = pokemon_has_abilities.drop_duplicates()

    # pokemon_evolves_to_pokemon
    pokemon_evolves_to_pokemon = pd.DataFrame()

    pokemon_to_id = pokemon.set_index("species")["ndex"].to_dict() # { pokemon_name: pokemon_id }
    temp = pokemon.copy()
    temp["pokemon_id"] = pokemon["pre-evolution"].map(pokemon_to_id)

    temp = temp.dropna(subset=["pokemon_id"])
    pokemon_evolves_to_pokemon = temp[["pokemon_id", "ndex"]].rename(columns={"ndex": "evolves_to"})
    pokemon_evolves_to_pokemon = pokemon_evolves_to_pokemon.drop_duplicates()
    pokemon_evolves_to_pokemon = pokemon_evolves_to_pokemon.rename(columns={"pokemon_id": "evolves_from"})

    # pokemon_has_types
    pokemon_has_types = pd.DataFrame()
    types_list = ["type1", "type2"]

    for type in types_list:
        temp = pd.merge(pokemon, types, left_on=type, right_on="type", how="right")
        temp = temp[["ndex", "type_id"]].rename(columns={"ndex": "pokemon_id"}).dropna()
        pokemon_has_types = pd.concat([pokemon_has_types, temp])
    pokemon_has_types = pokemon_has_types.drop_duplicates()

    # type_effectiveness
    type_effectiveness = pd.DataFrame()
    type_chart = type_chart.melt(id_vars=["defense-type1", "defense-type2"], var_name="attacking_type_id", value_name="multiplier")
    
    type_to_id = types_lowercase.set_index("type")["type_id"].to_dict() # { type: type_id }
    types_list = ["attacking_type_id", "defense-type1", "defense-type2"]
    type_chart[types_list] = type_chart[types_list].map(type_to_id.get)
    type_chart['defense-type2'] = type_chart['defense-type2'].astype('Int64')

    type_effectiveness = type_chart.dropna().drop_duplicates()
    type_effectiveness = type_effectiveness.rename(columns={"defense-type1": "defending_type_id", "defense-type2": "defending_type2_id"})

    ########## CLEANUP AND SENDING TO SQL SERVER ##########
    pokemon = cleanup.pokemon(pokemon)
    abilities = cleanup.abilities(abilities)
    types = cleanup.types(types)

    engine = create_engine("mysql+pymysql://root:root@localhost:3306/pokemon")

    resetDatabase(engine) # else foreign keys won't work, further explanation below @ why reset the database?)

    pokemon.to_sql("pokemon", con=engine, index=False, if_exists="append")
    abilities.to_sql("abilities", con=engine, index=False, if_exists="append")
    types.to_sql("types", con=engine, index=False, if_exists="append")

    pokemon_has_abilities.to_sql("pokemon_has_abilities", con=engine, index=False, if_exists="append")
    pokemon_evolves_to_pokemon.to_sql("pokemon_evolves_to_pokemon", con=engine, index=False, if_exists="append")
    pokemon_has_types.to_sql("pokemon_has_types", con=engine, index=False, if_exists="append")
    type_effectiveness.to_sql("type_effectiveness", con=engine, index=False, if_exists="append")

    print(f"sucessfully uploaded data to SQL server")

### explaining some stuff
# why reset the database?
# at first I thought that using "if_exists=replace" was a better idea, since using "if_exists=append"
# would try to re-add data that have already been added, conflicting with PKs (since it would re-send them).
# but using replace broke the relationships. The select queries still worked, but the relationship tables
# where now just mere tables created by pandas, meaning the IDs for the FKs weren't really FKs, just a
# number column. this would break if I try to add a repeated value there, for example.
# so, I wrote this script that just drops all tables in the database, then re-run the init.sql script.
# I then used "if_exists=append", because replace would drop the tables and default would cause an exception.

### for myself later (ignore)
# relations
# pd.merge(df_1, df_2, left_on="left_id", right_on="right_id")
# df.astype(type) (str | number -> type)
# pd.concat: https://pandas.pydata.org/docs/reference/api/pandas.concat.html
# df.melt: https://pandas.pydata.org/docs/reference/api/pandas.melt.html (IM SO GLAD I FOUND THIS)
# 
# json (pokemon moves)
# json.loads (str -> dic)
# df.apply: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.apply.html

csvToSQL()