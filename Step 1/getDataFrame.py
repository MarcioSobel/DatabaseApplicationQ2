import pandas as pd
from pandas import DataFrame
from typing import Literal
import os

def getDataFrame() -> DataFrame:

    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(script_directory, os.pardir, 'data')

    pokemons = pd.read_csv(f"{data_directory}/pokemon_data.csv", index_col=0)
    abilities = pd.read_csv(f"{data_directory}/ability.csv", index_col=0)
    stats = pd.read_csv(f"{data_directory}/stats.csv", index_col=0)

    pokemons = pd.merge(pokemons, abilities, on='pokedex_nr')
    pokemons = pd.merge(pokemons, stats, on='pokedex_nr')

    pokemons = removeColumns(pokemons)
    pokemons = renameColumns(pokemons)

    return pokemons

def removeColumns(dataFrame: DataFrame) -> DataFrame:
    return dataFrame.drop(columns=[
        # other languages
        'de_name',
        'type_1_german',
        'type_2_german',
        'type_list_ger',
        'fr_name',
        'jp_name',
        'kor_name',
        'chi_name',

        # not really necessary columns
        'link',
        'type_list',
        'ability.url',
        "('effort', 'attack')",
        "('effort', 'defense')",
        "('effort', 'hp')",
        "('effort', 'special-attack')",
        "('effort', 'special-defense')",
        "('effort', 'speed')",
    ])

def renameColumns(dataFrame: DataFrame) -> DataFrame:
    return dataFrame.rename(columns={
        "('base_stat', 'attack')": 'attack',
        "('base_stat', 'defense')": 'defense',
        "('base_stat', 'speed')": 'speed',
        "('base_stat', 'hp')": 'hp',
        "('base_stat', 'special-attack')": 'special_attack',
        "('base_stat', 'special-defense')": 'special_defense',
        'ability.name': 'ability_name',
    })