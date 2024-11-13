
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

class HotelDetailWithPrice(db.Model):
    __tablename__ = 'hotel_details_with_price'
    #id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255),primary_key = True)
    full_Name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    score = db.Column(db.String(255))
    reviews = db.Column(db.String(255))
    review_count = db.Column(db.String(255))
    details_URL = db.Column(db.String(1024))
    prices = db.Column(db.String(1024))

class HotelHistoryPrice(db.Model):
    __tablename__ = 'macau_hotel_price_history'
    month_index = db.Column(db.String(255),primary_key = True)
    three_star = db.Column(db.Float)
    four_star = db.Column(db.Float)
    five_star = db.Column(db.Float)
    average = db.Column(db.Float)
    month = db.Column(db.String(255))

class MacauEventsList(db.Model):
    __tablename__ = 'macau_events_list'
    id = db.Column(db.String(255),primary_key = True)
    month = db.Column(db.String(255))
    theme = db.Column(db.String(255))
    type = db.Column(db.String(64))
    start_date = db.Column(db.String(64))
    end_date = db.Column(db.String(64))
    intro = db.Column(db.String(2048))
    time = db.Column(db.String(255))
    location = db.Column(db.String(1024))
    fee = db.Column(db.String(1024))
    link = db.Column(db.String(255))
    facebook = db.Column(db.String(128))
    instagram = db.Column(db.String(64))
    wechat = db.Column(db.String(5))
    telephone = db.Column(db.String(255))
    email = db.Column(db.String(255))
    organise = db.Column(db.String(1024))
    longitude = db.Column(db.String(128))
    latitude = db.Column(db.String(255))
