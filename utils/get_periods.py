from requests import Session
from services.get_diary import get_diary
from utils.get_monday_date import get_monday_date
from datetime import date

def get_periods(session: Session, guid: str):
    diary = get_diary(session, guid, date=get_monday_date(date.today()))
    return diary['edu_periods']