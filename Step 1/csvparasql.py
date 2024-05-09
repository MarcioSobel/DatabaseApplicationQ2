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

moves = moves.rename(columns = {"id":"move_id"})

pokemon_possui_moves = pd.merge(pokemon,moves, left_on ="id", right_on = "move_id")

connection_string = "mysql+mysqlconnector://root:root@localhost:3306/pokemon"
engine = create_engine(connection_string)
sql_query = "SELECT * FROM pokemon"

df = pd.read_sql(sql_query, engine)

print(df)
            