from datetime import date as Date
from datetime import timedelta

def get_monday_date(today_date: Date):
    monday_date = today_date - timedelta(days=today_date.weekday())
    return monday_date