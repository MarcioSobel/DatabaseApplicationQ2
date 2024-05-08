import pandas as pd
import os
import csv

tabela_pokemon = pd.read_csv("pokemon_data.csv", sep=",")
tabela_ability = pd.read_csv("ability.csv", sep=",")
tabela_stats = pd.read_csv("stats.csv", sep=",")

pathName = os.getcwd()

numFiles = []
tabela_pokemon = os.listdir(pathName)
for tabela_pokemon in tabela_pokemon:
    if tabela_pokemon.endswith(".csv"):
        numFiles.append(tabela_pokemon)
for i  in numFiles:
    tabela_pokemon = open(os.path.join(pathName, i),"rU")    
reader = csv.reader(tabela_pokemon,delimiter=',')

for i in numFiles:
    file = open(os.path.join(pathName, i), "rU")
    reader = csv.reader(tabela_pokemon, delimiter=',')
    for row in reader:
        for column in row:
            print(column)
            if column=="SPECIFIC VALUE":
                #do stuff
