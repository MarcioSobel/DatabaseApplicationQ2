from sqlalchemy import Engine, MetaData, text

def resetDatabase(engine: Engine) -> None:
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.drop_all
    metadata.drop_all(bind=engine)
    
    with open("mysql/init.sql", "r") as file:
        sql_script = file.read()
    sql_statements = sql_script.split(";")

    with engine.connect() as connection:
        for statement in sql_statements:
            if (statement.strip()):
                connection.execute(text(statement))
