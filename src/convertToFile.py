import os
from pandas import DataFrame
from getDataFrame import *

def csvToSQL() -> None:
    items = getDataFrame("items.csv")
    moves = getDataFrame("moves.csv")
    natures = getDataFrame("natures.csv")
    pokedex = getDataFrame("pokedex.csv")
    pokemon = getDataFrame("pokemon.csv")
    movesets = getDataFrame("movesets.csv")
    abilities = getDataFrame("abilities.csv")
    type_chart = getDataFrame("type-chart.csv")

    directory = createDataDir()

    writeFile(directory, "items", items)
    writeFile(directory, "moves", moves)
    writeFile(directory, "natures", natures)
    writeFile(directory, "pokedex", pokedex)
    writeFile(directory, "pokemon", pokemon)
    writeFile(directory, "movesets", movesets)
    writeFile(directory, "abilities", abilities)
    writeFile(directory, "type_chart", type_chart)
    
    print(f"Successlly created files")

def writeFile(directory: str, tablename: str, dataFrame: DataFrame) -> None:
    with open(f"/{directory}/{tablename}.sql", "w") as file:
        for _, row in dataFrame.iterrows():
            rowValues = row.astype(str).values
            query = f"INSERT INTO {tablename} ({', '.join(dataFrame.columns)}) VALUES ({', '.join(rowValues)});\n"
            file.write(query)