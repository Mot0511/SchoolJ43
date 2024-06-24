from fastapi import APIRouter, Cookie, Depends, Form, Request, Response, status
from fastapi.responses import RedirectResponse
from auth.services import auth, get_guid
from auth.utils import get_session_id
from db.engine import get_async_session
from db.models import Session
from page_router import index
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

auth_router = APIRouter()

@auth_router.post('/auth', response_class=RedirectResponse)
async def auth_endpoint(request: Request, email: str = Form(...), password: str = Form(...), 
                  db_session: AsyncSession = Depends(get_async_session), 
                  guid: str | None = Cookie(default=None)):
    
    response = RedirectResponse('/home', status_code=status.HTTP_302_FOUND)
    
    if not guid:
        session = auth(email, password)

        guid = get_guid(session)
        session_id = get_session_id(session)

        session_model = Session(
            guid=guid,
            session_id=session_id
        )
        db_session.add(session_model)
        await db_session.commit()
        response.set_cookie(key='guid', value=guid, expires=datetime.now(timezone.utc) + timedelta(days=365))

    return response