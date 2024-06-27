from datetime import date, datetime
from typing import List
from requests import Session

from services.get_diary import get_diary
from utils.get_monday_date import get_monday_date


def get_week_marks(session: Session, guid: str) -> List[int]:
    
    marks = []

    diary = get_diary(session, guid, '01.03.2024')['diary']
    # diary = get_diary(session, guid, get_monday_date(date.today()))['diary']
    for day in diary:
        for lesson in day['lessons']:
            for mark in lesson['marksRaw']:
                marks.append(mark)

    return marks