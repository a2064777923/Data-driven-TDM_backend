import calendar
from datetime import datetime

from flask import jsonify
from app import db
from app.event_overview import event_bp
from app.models import FestivalEvent


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