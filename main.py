import json

from repository import BeerRepository, BeerDataBaseRepository
from beer import Beer
from flask import Flask, request, abort
from util import validate_alc_content, validate_beer_brand
from sqlalchemy import create_engine
from beer_db import BeerDataBase, BeerModel

beer_repository = BeerRepository("beers.json")

engine = create_engine("mysql+mysqlconnector://root:passlocalhost/girrafe")
beer_repository_db = BeerDataBaseRepository(engine)
BeerDataBase.metadata.create_all(engine)

app = Flask(__name__)
url = "https://raw.githubusercontent.com/lvarayut/beergallery/master/public/data/beer.json"

all_beers = beer_repository_db.get_beers(url)
print(all_beers)


def create_error_message(msg, status_code: int):
    return json.dumps({"error": f"{msg}"}), status_code


@app.after_request
def add_header(response):
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route("/beer", methods=['POST'])
def create_beer_handler():
    json_data = request.get_json()
    beer_id = json_data.get("id")
    alc_cont = json_data.get("alcoholic_contents")
    beer_brand = json_data.get("brand")
    detail = json_data.get("detail")
    country_origin = json_data.get("country_origin")
    if not validate_beer_brand(beer_brand):
        return create_error_message("Invalid brand name", 400)
    if not validate_alc_content(alc_cont):
        return create_error_message("Invalid alcoholic content", 400)
    beer = Beer(json_data["id"], beer_brand, alc_cont, detail, country_origin)
    created_beer = beer_repository_db.create_beer(beer)
    return json.dumps(created_beer.__dict__)


@app.route("/beer/<beer_id>", methods=['GET'])
def find_beer_by_id_handler(beer_id):
    found_beer = beer_repository_db.find_beer_by_id(beer_id)
    if found_beer:
        return json.dumps(found_beer.__dict__)
    else:
        return create_error_message("ID not found", 404)


@app.route("/beer/<beer_id>", methods=['DELETE'])
def delete_beer_by_id_handler(beer_id):
    if beer_repository_db.delete_beer(beer_id) > 0:
        return f"Beer {beer_id} deleted."
    else:
        return create_error_message("ID not found", 404)


@app.route("/beer/<beer_id>", methods=['PUT'])
def update_beer_handler(beer_id):
    json_data = request.get_json()
    alc_cont = json_data["alcoholic_contents"]
    beer_brand = json_data["brand"]
    if not validate_beer_brand(beer_brand):
        return create_error_message("Invalid brand name", 400)
    if not validate_alc_content(alc_cont):
        return create_error_message("Invalid alcoholic content", 400)
    beer = Beer(json_data["id"], beer_brand, alc_cont)
    updated_beer = (beer_repository_db.update_beer(beer_id, beer))
    if updated_beer:
        return json.dumps(updated_beer.__dict__)
    else:
        return create_error_message("Beer not found", 404)


@app.route("/beer/brand/<brand_name>", methods=['GET'])
def find_beer_by_brand_name_handler(brand_name):
    found_beers = beer_repository_db.find_by_brand_name(brand_name)
    found_beers = [beer.__dict__ for beer in found_beers]
    return json.dumps(found_beers)


if __name__ == "__main__":
    app.run()
