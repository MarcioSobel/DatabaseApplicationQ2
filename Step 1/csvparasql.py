import pandas as pd
import os
from sqlalchemy import create_engine, text

script_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(script_directory, os.pardir, 'data')

pokemons = pd.read_csv(f"{data_directory}/pokemon_data.csv")
moves = pd.read_csv(f"{data_directory}/ability.csv")
stats = pd.read_csv(f"{data_directory}/stats.csv")

pokemons = pd.merge(pokemons, moves, on='pokedex_nr')
pokemons_final = pd.merge(pokemons, stats, on= 'pokedex_nr')
pokemons_final.drop(index=0)

tablename = "tabela_de_pokemons"
with open(f'{tablename}.sql', 'w', encoding='utf-8') as file:
        for _, row in pokemons_final.iterrows():
            query = f"INSERT INTO {tablename} ({', '.join(pokemons.columns)}) VALUES ({', '.join(row.astype(str).values)});\n"
            file.write(query)