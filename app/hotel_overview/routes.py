from flask import jsonify
from app import db
from app.hotel_overview import hotel_bp
from app.models import Hotel


@hotel_bp.route('/getHotelsCount', methods=['GET'])
def hotel_overview():
    hotels = db.session.query(Hotel.classname_en, db.func.count(Hotel.id).label('count')).group_by(Hotel.classname_en).all() # 以酒店類型分組計算每類酒店的數量

    overview = {hotel.classname_en: hotel.count for hotel in hotels}
    total_count = sum(overview.values())

    overview['total'] = total_count
    result = {"success": True, "data":overview}
    # 返回json數據
    return jsonify(result)
