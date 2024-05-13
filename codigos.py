import os
import pandas as pd
import numpy as np
tabela_pokemon = pd.read_csv("data/pokemon.csv")
tabela_explication_moves = pd.read_csv("data/moves.csv")
tabela_pokedex = pd.read_csv("data/pokedex.csv")
tabela_pokedesc = pd.read_csv("data/poki_descs.csv")
tabela_abilities = pd.read_csv("data/abilities.csv")

tabela_TM = pd.merge(tabela_pokemon,tabela_pokedex, left_on= "ndex", right_on= "Id", how="left")
tabela_TM = tabela_TM.drop(columns=["Id"])
tabela_ALL = pd.merge(tabela_TM, tabela_explication_moves, left_on= "ndex", right_on= "id", how="left")
tabela_ALL = pd.merge(tabela_ALL, tabela_pokedesc, left_on= "Name", right_on= "name", how="left")
print (tabela_ALL.head(5))
#------------------------------------------------------------------------------------------------------------------