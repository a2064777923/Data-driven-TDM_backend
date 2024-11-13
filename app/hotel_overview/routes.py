from flask import jsonify
from app import db
from app.hotel_overview import hotel_bp
from app.models import Hotel, HotelHistoryPrice


@hotel_bp.route('/getHotelsCount', methods=['GET'])
def hotel_overview():
    hotels = db.session.query(Hotel.classname_en, db.func.count(Hotel.id).label('count')).group_by(Hotel.classname_en).all() # 以酒店類型分組計算每類酒店的數量

    overview = {hotel.classname_en: hotel.count for hotel in hotels}
    total_count = sum(overview.values())

    overview['total'] = total_count
    result = {"success": True, "data":overview}
    # 返回json數據
    return jsonify(result)

@hotel_bp.route('/getHotelPriceHistory',methods=['GET'])
def hotel_price():
    results = db.session.query(
        HotelHistoryPrice.month,
        HotelHistoryPrice.three_star,
        HotelHistoryPrice.four_star,
        HotelHistoryPrice.five_star,
        HotelHistoryPrice.average
    ).all()

    data = {
            'month': [result.month for result in results],
            'three_star': [result.three_star for result in results],
            'four_star': [result.four_star for result in results],
            'five_star': [result.five_star for result in results],
            'average': [result.average for result in results],
        }
    return jsonify({"success":True,"data":data})