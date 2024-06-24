from calendar import week
from datetime import date, datetime
from re import L
from fastapi import APIRouter, Cookie, Request
from fastapi.templating import Jinja2Templates
from auth.utils import get_session
from services.get_diary import get_diary
from services.get_marks import get_marks
from utils.count_of_entry import count_of_entry
from utils.get_monday_date import get_monday_date
from utils.get_periods import get_periods
from utils.get_week_marks import get_week_marks

page_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@page_router.get('/')
def login(request: Request):
    return templates.TemplateResponse(request=request, name='login.html')

@page_router.get('/home')
async def index(request: Request, guid: str | None = Cookie(default=None)):
    session = await get_session(guid)
    diary = get_diary(session, guid, date.today())['diary']
    today = (diary[0] if diary else None)

    count_week_marks = get_week_marks(session, guid)
    week_marks = {
        'marks': count_week_marks,
        'count5': count_of_entry(count_week_marks, '5'),
        'count4': count_of_entry(count_week_marks, '4'),
        'count3': count_of_entry(count_week_marks, '3'),
        'count2': count_of_entry(count_week_marks, '2'),
        'count1': count_of_entry(count_week_marks, '1'),
    }
    print(week_marks)

    return templates.TemplateResponse(request=request, name='index.html', context={'title': 'Главная', 'today': today, 'week_marks': week_marks})

@page_router.get('/diary')
async def diary(request: Request, date: str = get_monday_date(date.today()).strftime('%d.%m.%Y'), guid: str | None = Cookie(default=None)):
    session = await get_session(guid)
    diary = get_diary(session, guid, get_monday_date(datetime.strptime(date, '%d.%m.%Y').date()))['diary']
    
    leftColumn = []
    if diary:
        for i in range(3):
            leftColumn.append(diary[i])
        
        for day in leftColumn:
            diary.remove(day)

    
    return templates.TemplateResponse(request=request, name='diary.html', context={'title': 'Дневник', 'leftColumn': leftColumn, 'rightColumn': diary})

@page_router.get('/marks/{quarter}')
async def marks(request: Request, quarter: str, guid: str | None = Cookie(default=None)):
    session = await get_session(guid)
    period = get_periods(session, guid)[(int(quarter) if int(quarter) <= 4 else 4) - 1]
    marks = get_marks(session=session, guid=guid, begin=period['dateBegin'], end=period['dateEnd'])

    return templates.TemplateResponse(request=request, name='marks.html', context={'title': 'Оценки', 'marks': marks, 'period': period})