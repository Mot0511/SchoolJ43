from functools import wraps
from auth.utils import get_session
from db.engine import sessionmaker

from fastapi import Cookie

def auth_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        guid = kwargs['guid']
        db_session = await sessionmaker()
        session = await get_session(guid, db_session)

        auth_data = {
            'session': session,
            'guid': guid
        }

        kwargs['auth_data'] = auth_data

        return await func(*args, **kwargs)

    return wrapper
