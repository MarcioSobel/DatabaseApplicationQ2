from pandas import DataFrame
from getDataFrame import *

def csvToSQL() -> None:
    pokemons = getDataFrame(type='json')

    with open(f"pokemon.sql", 'w') as file:
        for _, row in pokemons.iterrows():
            rowValues = row.astype(str).values
            query = f"INSERT INTO pokemon ({', '.join(pokemons.columns)}) VALUES ({', '.join(rowValues)});\n"
            file.write(query)
    
    print(f"Successlly created file pokemon.sql")