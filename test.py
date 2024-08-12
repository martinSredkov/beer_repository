from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, select
from beer_db import BeerDataBase, BeerModel
# Connect to the database
engine = create_engine("mysql+mysqlconnector://root:asd255@localhost/girrafe")

# Test the connection
connection = engine.connect()
BeerDataBase.metadata.create_all(engine)

with Session(engine) as session:
    ariana = BeerModel(
        brand="zagorka",
        alcoholic_content = 6.4
    )

    session.add(ariana)
    session.commit()
    # ariana = session.query(BeerModel).filter(BeerModel.id == 1).first()
    # ariana.id.remove(1)
    # ariana.brand = "Zagorka"
    # session.delete(ariana)
    # session.commit()
    # ariana = session.query(BeerModel).filter(BeerModel.brand == "Zagorka").first()
    # print(ariana)

