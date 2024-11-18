import json

from flask import jsonify, request
import random

from sqlalchemy import false

from app import db
from app.map_business import map_bp
from app.models import HotelDetailWithPrice


def generate_data_list(count, max_value):
    macau_region = ["花地玛堂区", "圣安多尼堂区", "大堂区", "望德堂区", "风顺堂区", "嘉模堂区", "圣方济各堂区",
                    "路氹填海区"]
    data_list = []
    used_names = set()
    while len(data_list) < count:
        name = random.choice(macau_region)
        if name not in used_names:
            data_list.append({
                "name": name,
                "value": random.randint(1, max_value)
            })
            used_names.add(name)
    return data_list

@map_bp.route('/getCenterMap', methods=['GET'])
def center_map():
    region_code = "Macau"
    if region_code and region_code != "Macau":
        data_list = generate_data_list(8, 1000)
        response_data = {
            "success": True,
            "data": {
                "dataList": data_list,
                "regionCode": region_code
            }
        }
    else:
        data_list = generate_data_list(8, 1100)
        response_data = {
            "success": True,
            "data": {
                "dataList": data_list,
                "regionCode": "Macau"
            }
        }
    return jsonify(response_data)

@map_bp.route('/getHotelMapDetail', methods=['GET'])
def get_hotel_map_detail():
    hotel_result={"data":{},"success":True}
    hotelName = request.args.get('hotelName')
    hotels_detail = HotelDetailWithPrice.query.filter_by(name = hotelName).first()
    if hotels_detail == None:
        hotel_result["success"] = False
        return jsonify(hotel_result)
    if hotels_detail.details_URL == "nan":
        hotel_result["success"] = False
        return jsonify(hotel_result)
    else:
        hotelData = None
        try:
            hotelDetail ={"fullName": hotels_detail.full_Name,
                          "description":hotels_detail.description,
                          "score":hotels_detail.score,
                          "reviews":hotels_detail.reviews,
                          "reviewCount": hotels_detail.review_count,
                          "hotelURL": hotels_detail.details_URL,
                          "prices":hotels_detail.prices,
                          "sameStandandPriceLastYearThisMonth": 1902.5,
                          "averagePriceLastYearThisMonth":894.3,
                          "sameStandandPriceOverHistory":991.4,
                          }
            with open('./data/hotel_reviews_adjective.json', 'r', encoding='utf-8') as file:
                adjective_data = json.load(file)
            with open('./data/hotel_reviews_noun.json', 'r', encoding='utf-8') as file:
                noun_data = json.load(file)
            hotelData = {"hotelDetail":hotelDetail, "hotelReviews":{"hotelName":hotelName,"adjectives":adjective_data[hotelName],"nouns":noun_data[hotelName][0:10]}}
            hotel_result["data"] = hotelData
        except (NotADirectoryError, KeyError) as e:
            print("can't find file")
            hotel_result["success"] = False
            return jsonify(hotel_result)
    return jsonify({"data":hotelData,"success":True})

