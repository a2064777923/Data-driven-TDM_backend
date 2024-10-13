
from app import db

class Hotel(db.Model):
    __tablename__ = 'hotel_detail'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    classname_en = db.Column(db.String(50))

class MainlandTourist(db.Model):
    __tablename__ = 'mainland_visitor_distribute_stats'

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer)
    china_en = db.Column(db.String(128))
    district_en = db.Column(db.String(128))
    persontime = db.Column(db.Integer)


class FestivalEvent(db.Model):
    __tablename__ = 'festival_event_table'
    id = db.Column(db.Integer, primary_key = True)
    name_en = db.Column(db.String(128))
    showDate = db.Column(db.String(128))
    isPublicHoliday = db.Column(db.String(5))
    link = db.Column(db.String(128))

class AverageLengthStayVisitors(db.Model):
    __tablename__ = 'average_length_stay_visitors'
    id = db.Column(db.Integer,primary_key = True)
    period = db.Column(db.String(64))
    value = db.Column(db.Float)