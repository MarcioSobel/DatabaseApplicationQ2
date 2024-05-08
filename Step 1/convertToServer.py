from sqlalchemy import create_engine
from getDataFrame import *

def csvToSQL() -> None:
    pokemons = getDataFrame(type='json')
    engine = create_engine('mysql+pymysql://root:root@localhost:3306/pokemons')

    pokemons.to_sql('pokemon', con=engine, index=False)

    print(f"sucessfully uploaded data to SQL server")
