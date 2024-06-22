from fastapi import Depends
import requests
from sqlalchemy import select

from auth.services import get_header
from db.engine import sessionmaker
from db.models import Session

def get_session_id(session: Session) -> str | None:
    cookie = next((i for i in session.cookies if i.name == 'X1_SSO'), None)
    return cookie.value if cookie else None

async def get_session(guid: str) -> Session:
    async with sessionmaker() as db_session:
        q = select(Session.session_id).where(Session.guid == guid)
        res = await db_session.execute(q)
        session_id = res.scalar()

        cookies = {'X1_SSO': session_id}

        session = requests.Session()
        session.headers.update(get_header())
        session.cookies.update(cookies)
        session.get("https://one.43edu.ru/")

    return session