from flask import jsonify
import random
from app.map_business import map_bp


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