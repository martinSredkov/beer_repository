import json
import requests
from beer import Beer
from sqlalchemy.orm import Session
from sqlalchemy import Engine
from beer_db import BeerModel


class BeerDataBaseRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.session = Session(engine)

    def create_beer(self, beer_data: Beer):
        new_beer = self.map_dto_to_model(beer_data)
        self.session.add(new_beer)
        self.session.commit()
        return self.map_model_to_dto(new_beer)

    def update_beer(self, id: int, beer_data: Beer):
        found_beer = self.session.query(BeerModel).filter(BeerModel.id == id).first()
        found_beer.brand = beer_data.brand
        found_beer.alcoholic_content = beer_data.alcoholic_content
        self.session.commit()
        return self.find_beer_by_id(id)

    def find_beer_by_id(self, id: int):
        found_beer = self.session.query(BeerModel).filter(BeerModel.id == id).first()
        if not found_beer:
            return None
        return self.map_model_to_dto(found_beer)

    def delete_beer(self, id: int):
        found_beer = self.session.query(BeerModel).filter(BeerModel.id == id).first()
        if found_beer:
            self.session.delete(found_beer)
            self.session.commit()
            return int(id)
        else:
            return -1

    def get_beers(self, url):
        new_beers = requests.get(url).json()
        for beer in new_beers:
            country_name = beer["country"]["name"] if isinstance(beer["country"], dict) else beer["country"]

            new_beer_data = BeerModel(
                id=beer["id"],
                brand=beer["name"],
                alcoholic_content=beer["abv"],
                detail=beer["detail"],
                country_origin=country_name
            )
            self.session.add(new_beer_data)
        self.session.commit()
        return new_beers

    def find_by_brand_name(self, name):
        found_beers = self.session.query(BeerModel).filter(BeerModel.brand.like(f"%{name}%")).all()
        if not found_beers:
            return []
        return [self.map_model_to_dto(beer) for beer in found_beers]

    def map_model_to_dto(self, beer):
        mapped_beer = Beer(id=beer.id, brand=beer.brand, alcoholic_content=beer.alcoholic_content, detail=beer.detail, country_origin=beer.country_origin)
        return mapped_beer

    def map_dto_to_model(self, beer):
        beer = BeerModel(id=beer.id, brand=beer.brand, alcoholic_content=beer.alcoholic_content, detail=beer.detail, country_origin=beer.country_origin)
        return beer


class BeerRepository:
    def __init__(self, file):
        self.file = file
        self.list_of_beers = []

    def create_beer(self, beer_data: Beer):
        self.load()
        beer_data.id = len(self.list_of_beers) + 1
        self.list_of_beers.append(beer_data)
        self.flush()

    def update_beer(self, id: int, beer_data: Beer):
        self.load()
        for el in self.list_of_beers:
            if el.id == int(id):
                el.brand = beer_data.brand
                el.alcoholic_content = beer_data.alcoholic_content
                self.flush()
                return el

        return None

    def find_beer_by_id(self, id: int):
        self.load()
        for el in self.list_of_beers:
            if el.id == int(id):
                return el

        return None

    def delete_beer(self, id: int):
        self.load()
        deleted_beer = -1
        for el in self.list_of_beers:
            if el.id == int(id):
                self.list_of_beers.remove(el)
                deleted_beer = el.id
        self.flush()
        return deleted_beer

    def load(self):
        self.list_of_beers = []
        with open(self.file, "r") as data:
            contents = data.read()
            list_of_beers = json.loads(contents)
            for beer_dict in list_of_beers:
                beer = Beer(beer_dict["id"], beer_dict["brand"], beer_dict["alcoholic_contents"])
                self.list_of_beers.append(beer)

    def flush(self):
        with open(self.file, "w") as data:
            json_dumps = json.dumps([el.__dict__ for el in self.list_of_beers])
            data.write(json_dumps)

    def find_by_alc_percent(self, percent):
        found_beers = []
        self.load()
        for el in self.list_of_beers:
            if el.alcoholic_content <= int(percent):
                found_beers.append(el)
        return found_beers

    def find_by_brand_name(self, name):
        found_beers = []
        self.load()
        for el in self.list_of_beers:
            if el.brand.__contains__(name):
                found_beers.append(el)
        return found_beers

