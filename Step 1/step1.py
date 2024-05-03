import pandas as pd
import os

def csvToSQL(table_name):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(script_directory, os.pardir, 'data')

    pokemons = pd.read_csv(f'{data_directory}/pokemon_data.csv', index_col=0)
    abilities = pd.read_csv(f'{data_directory}/ability.csv', index_col=0)
    stats = pd.read_csv(f'{data_directory}/stats.csv', index_col=0)

    pokemons = pd.merge(pokemons, abilities, on='pokedex_nr')
    pokemons = pd.merge(pokemons, stats, on='pokedex_nr')

    print(pokemons)

    with open(f'{table_name}.sql', 'w') as file:
        for _, row in pokemons.iterrows():
            query = f"INSERT INTO {table_name} ({', '.join(pokemons.columns)}) VALUES ({', '.join(row.astype(str).values)});\n"
            file.write(query)