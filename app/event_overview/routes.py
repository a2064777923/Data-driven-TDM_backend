import calendar
import re
from datetime import datetime

import pandas as pd
from flask import jsonify

from app import db
from app.event_overview import event_bp
from app.models import FestivalEvent, MacauEventsList


def get_weekday(date_str):
    date_parts = date_str.split('~')[0]  # Get the start date if it's a range
    date_obj = datetime.strptime(date_parts, '%Y-%m-%d')
    return calendar.day_name[date_obj.weekday()]

def map_holiday(is_public_holiday):
    return "Public Holiday" if is_public_holiday == 'Y' else "Not Holiday"


@event_bp.route('/getFestivalEvents', methods=['GET'])
def get_festival_events():
    datas = []
    events = db.session.query(
        FestivalEvent.name_en,
        FestivalEvent.showDate,
        FestivalEvent.isPublicHoliday,
        FestivalEvent.link
    ).all()
    for event in events:
        data = {"name_en": event[0] , "showDate":event[1],"isPublicHoliday":event[2], "link": event[3]}
        datas.append(data)

    print(datas)
    for event in datas:
        # event['weekDay'] = get_weekday(event['showDate'])不行，有的是持續多日的
        event['isPublicHoliday'] = map_holiday(event['isPublicHoliday'])

    datas.sort(key=lambda x: x['showDate'])
    recent_events = datas[:5]
    remaining_events = datas[5:]
    remaining_events.sort(key=lambda x: x['showDate'], reverse=True)

    result = recent_events + remaining_events
    return jsonify({"data":result,"success":True})

def normalize_end_date(end_date, month):
    if pd.isna(end_date):
        # 如果是NaN，用month代替
        return '30/' + month.split('/')[1] + '/'  + month.split('/')[0]
    # 用,;分割取最后一个日期
    dates = re.split(r'[;,]', end_date)
    date = dates[-1].strip()
    # 如果日期是日/月格式，返回，否则用month代替
    if re.match(r'\d{1,2}/\d{1,2}', date):
        return date + month.split('/')[0]
    else:
        return '30/' + month.split('/')[1] + '/' + month.split('/')[0]

@event_bp.route('/getEventsHolding',methods=['GET'])
def get_events_holding():
    events = MacauEventsList.query.all()
    today = datetime.now()
    filtered_events = []

    for event in events:
        normalized_end_date = normalize_end_date(event.end_date, event.month)
        try:
            end_date_obj = datetime.strptime(normalized_end_date, '%d/%m/%Y')
            if end_date_obj > today:
                event_data = {
                    "id": event.id,
                    "month": event.month,
                    "theme": event.theme,
                    "type": event.type,
                    "start_date": event.start_date,
                    "end_date": normalized_end_date.split("/2")[0],
                    "intro": event.intro,
                    "time": event.time,
                    "location": event.location,
                    "fee": event.fee,
                    "link": event.link,
                    "facebook": event.facebook,
                    "instagram": event.instagram,
                    "wechat": event.wechat,
                    "telephone": event.telephone,
                    "email": event.email,
                    "organise": event.organise,
                    "longitude": event.longitude,
                    "latitude": event.latitude,
                    "imageURL":f"https://img.macautourism.top/tourism/tourism/assert/2024/11/12/{event.id}.jpeg"
                }
                filtered_events.append(event_data)
        except ValueError:
            continue

    return jsonify({"data": filtered_events,"success":True})