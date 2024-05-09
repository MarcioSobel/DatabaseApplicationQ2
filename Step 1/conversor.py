import pandas as pd # type: ignore
import os 

script_directory = os.path.dirname(os.path.abspath(__file__))
data_directory = os.path.join(script_directory, os.pardir, 'data')

pokemongos = pd.read_csv(f"{data_directory}/pokemon_data.csv")
Habilimongos = pd.read_csv(f"{data_directory}/ability.csv")
status = pd.read_csv(f"{data_directory}/stats.csv")

uniao = pokemongos.merge(status, how='left' , on='pokedex_nr')
uniao_Final = uniao.merge(Habilimongos, how='left', on='pokedex_nr')



with open(f"banco.sql", "w", encoding="utf-8") as file:

    for _, rows in uniao_Final.iterrows():
        
            from string import Template
        
            banco = Template("INSERT INTO TABLE VALUES($valores)")
            file.write(banco.substitute({"valores":rows.astype(str).values}))