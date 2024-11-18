import random

from flask import jsonify
from sqlalchemy import func

from app import db
from app.tourist_overview import tourist_bp
from app.models import MainlandTourist, AverageLengthStayVisitors, EntryAndExit
import numpy as np
from collections import defaultdict

@tourist_bp.route('/getMainlandTourist', methods=['GET'])
def calculate_mainland_tourist_statistics():
    data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    rows = db.session.query(
        MainlandTourist.month,
        MainlandTourist.china_en,
        MainlandTourist.district_en,
        MainlandTourist.persontime
    ).all()
    # Aggregate data
    for  month, china_en, district_en, person_time in rows:
        data[district_en][china_en][month].append(person_time)

    result = {}

    # Calculate statistics
    for district, provinces in data.items():
        result[district] = []
        for province, months in provinces.items():
            monthly_counts = [sum(months[month]) for month in sorted(months)]
            total = sum(monthly_counts)
            mean = np.mean(monthly_counts)
            median = np.median(monthly_counts)
            variance = np.var(monthly_counts)
            max_month = max(months, key=lambda month: sum(months[month]))
            min_month = min(months, key=lambda month: sum(months[month]))

            result[district].append({
                province: {
                    '總人數': total,
                    '最多人月份': f"{max_month}: {sum(months[max_month])}人",
                    '最少人月份': f"{min_month}: {sum(months[min_month])}人",
                    '均值': mean,
                    '中位數': median,
                    '方差': variance,
                    '以月份排人數列表': monthly_counts
                }
            })

    print(result)
    # Sort data by total visitor count for districts
    # 這段真是搞死人了，邏輯很容易卡，最好別亂動
    result = dict(sorted(result.items(), key=lambda item : sum(list(province_data.values())[0].get("總人數")for province_data in item[1]), reverse=True))

    return jsonify({"data": result, "success": True})


def random_num_both(min_val, max_val):
    return random.randint(min_val, max_val)

@tourist_bp.route('/getCenterBottomMock')
def get_center_bottom_mock():
    regions = [
        "Huadima Parish", "San Antonio Parish", "Lobby", "Wangde Parish",
        "Fengshun Parish", "Jiamo Parish", "San Franciscan Parish", "Cotai Reclamation Area"
    ]

    num = random_num_both(26, 32)

    category = random.choices(regions, k=num)
    bar_data = [random.randint(10, 100) for _ in range(num)]

    line_data = []
    rate_data = []

    for index in range(num):
        line_num = random.randint(0, 100) + bar_data[index]
        line_data.append(line_num)
        rate = bar_data[index] / line_num
        rate_data.append(f"{(rate * 100):.0f}")

    mock_data ={
        "category": category,
        "barData": bar_data,
        "lineData": line_data,
        "rateData": rate_data
    }
    return jsonify(success=True, data=mock_data)

@tourist_bp.route('/getAverageLengthStay')
def get_average_length_stay():
    date_list = []
    num_list1 = []
    num_list2 = []
    rows = db.session.query(
        AverageLengthStayVisitors.period,
        AverageLengthStayVisitors.value
    ).all()

    month_mapping = {
        "1月": "January", "2月": "February", "3月": "March",
        "4月": "April", "5月": "May", "6月": "June",
        "7月": "July", "8月": "August", "9月": "September",
        "10月": "October", "11月": "November", "12月": "December"
    }


    # 过滤掉没有月份的数据，并转换时间格式
    for record in rows:
        if "月" in record.period:
            year = record.period[:4]
            month_chinese = record.period[5:]
            month_english = month_mapping.get(month_chinese, "")
            if month_english:
                date_list.append(f"{month_english} {year}")
                num_list1.append(record.value)
                num_list2.append(round(random.uniform(1.0, 2.0),2))  # 随机填充

    response = {
        "data": {
            "dateList": date_list,
            "numList1": num_list1,
            "numList2": num_list2
        },
        "success": True
    }
    return jsonify(response)

@tourist_bp.route("/getEnterExitMock")
def get_Enter_Exit_Mock():
    # 定义口岸列表
    checkpoints = [
        "Outer Harbour",
        "Inner Harbour",
        "Border Gate",
        "Macau International Airport",
        "Cotai Lotus Bridge Border Crossing",
        "Zhuhai-Macao Cross-border Industrial Zone",
        "Taipa Ferry Terminal",
        "Hong Kong-Zhuhai-Macao Bridge",
        "Qingmao"
    ]

    # 定义年份范围
    years = range(2019, 2025)

    # 查询数据库并汇总数据
    results = (
        db.session.query(
            EntryAndExit.year,
            EntryAndExit.placeEN,
            func.sum(EntryAndExit.number).label('total_number')
        )
        .filter(EntryAndExit.year.in_(years))
        .group_by(EntryAndExit.year, EntryAndExit.placeEN)
        .all()
    )

    # 初始化数据存储结构
    data = {}
    for year, placeEN, total_number in results:
        if str(year) not in data:
            data[str(year)] = {'total': 0, 'entries': []}  # 存储总人数和每个口岸的条目

        # 更新年总人数
        data[str(year)]['total'] += total_number

        # 检查口岸是否已经在该年份的数据中存在
        existing_entry = next((item for item in data[str(year)]['entries'] if placeEN in item), None)

        if existing_entry:
            # 如果已存在，则将出入境人数合并
            existing_entry[placeEN]['出入境人數'] += total_number
        else:
            # 否则，添加新条目
            data[str(year)]['entries'].append({
                placeEN: {
                    "出入境人數": total_number,
                    "在當年總人數中所佔百分比": 0  # 占比，待后续计算
                }
            })

    # 计算百分比
    for year in data:
        total_population = data[year]['total']
        for entry in data[year]['entries']:
            for place, info in entry.items():
                info['在當年總人數中所佔百分比'] = round((info['出入境人數'] / total_population) * 100, 2)

        # 清理数据结构，移除总人数信息
        data[year] = data[year]['entries']

    # 包装结果为JSON格式
    result = {
        "data": data,
        "success": True
    }
    return jsonify(result)

@tourist_bp.route("/getRankingData")
def generate_ranking_mock_data():
    # 定义出行方式列表
    transport_modes = [
        "Bus",
        "Train",
        "Airplane",
        "Bicycle",
        "Car",
        "Boat",
        "Walk",
        "Subway",
        "Tram",
        "Helicopter"
    ]

    # 随机生成数据
    num = [{"value": random.randint(50, 1000), "name": random.choice(transport_modes)} for _ in range(80)]

    # 筛选出最多8个不同的出行方式
    new_num = []
    num_obj = {}
    for item in num:
        if item["name"] not in num_obj and len(new_num) < 8:
            num_obj[item["name"]] = True
            new_num.append(item)

    # 按照 value 降序排序
    arr = sorted(new_num, key=lambda x: x["value"], reverse=True)

    # 构造返回结果
    result = {
        "success": True,
        "data": arr
    }
    return jsonify(result)
