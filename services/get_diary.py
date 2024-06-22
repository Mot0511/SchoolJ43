from typing import Union
import requests
from auth.utils import get_session_id
from datetime import date as d
import logging

def get_diary(session: requests.Session, guid: str, date: str,
                  retry=True) -> Union[tuple[None, None], tuple[dict, requests.Session]]:
    """
    Получает данные о неделе

    :param session: Сессия пользователя
    :param guid: Guid пользователя
    :param date: Дата для получения
    :param retry: Пытаться ли переподключиться в случае ошибки
    :return: Кортеж из json ответа от one.43edu.ru и сессии. В ответе содержатся дни от заданного до конца недели, а
         также данные об учебных периодах
    """
    
    response = session.get("https://one.43edu.ru/edv/index/diary/" + guid, params={'date': date})
    json = response.json()

    if json["success"]:

        diary = json['data']

        if diary['diary']:
            week = []
            for day, lessons in diary['diary'].items():
                week.append({'day': day, 'lessons': lessons})

            diary['diary'] = week
        
        return diary

    # sess_cookie = get_session_id(session)
    # user = db.session.query(User).filter(User.source_session == sess_cookie).first()
    # if retry:
    #     sess = auth(user.email, user.get_password())
    #     if sess is None:
    #         remove_user(user)
    #         return None, None
    #     cookie = get_session_cookie(sess)
    #     user.source_session = cookie
    #     db.session.merge(user)
    #     db.session.commit()

    #     raw_diary, _ = get_raw_diary(sess, guid, date, retry=False)
    #     return raw_diary, sess
    logging.error(f"Ошибка при получении данных. Сообщение: {json['message']}, guid: {guid}, "
                  f"session cookies: {session.cookies}")
    return None, None