import math
import pandas as pd
import os
import _mysql_connector
from sqlalchemy import create_engine, text


script_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(script_directory, os.pardir, 'data')

abilities = pd.read_csv(f"{data_directory}/abilities.csv")
items = pd.read_csv(f"{data_directory}/items.csv")
moves = pd.read_csv(f"{data_directory}/moves.csv")
movesets = pd.read_csv(f"{data_directory}/movesets.csv")
natures = pd.read_csv(f"{data_directory}/natures.csv")
pokedex = pd.read_csv(f"{data_directory}/pokedex.csv")
pokemon = pd.read_csv(f"{data_directory}/pokemon.csv")
type = pd.read_csv(f"{data_directory}/type-chart.csv")


moves = moves.rename(columns={"id":"move_id"})

#abilities = abilities.drop(columns=["description"])

pokemon_has_abilities = pd.DataFrame()
abilities_list = ["ability1","ability2","abilityH"]

for ability in abilities_list:
    temp = pd.merge(pokemon,abilities, left_on=ability, right_on="ability", how="left")
    temp = temp[["ndex", "ability"]].rename(columns={"ndex": "pokemon_id"}).dropna()
    pokemon_has_abilities = pd.concat([pokemon_has_abilities, temp])
pokemon_has_abilities = pokemon_has_abilities.drop_duplicates()





connection_string = "mysql+mysqlconnector://root:root@localhost:3306/pokemon"
engine = create_engine(connection_string)

pokemon_has_abilities.to_sql("teste",con=engine,if_exists="replace",index=False)


#print(pokemon_has_abilities)

print("Aplicação feita")

