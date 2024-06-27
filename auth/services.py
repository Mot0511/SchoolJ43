from typing import Optional
from bs4 import BeautifulSoup
from fastapi import requests
import requests
from fake_useragent import UserAgent

ua = UserAgent()

def get_header() -> dict:
    """
    Возвращает случайный заголовок с User-Agent
    """
    return {'User-Agent': str(ua.random)}


def auth(login: str, password: str) -> Optional[requests.Session]:
    session = requests.Session()
    session.headers.update(get_header())

    url = 'https://passport.43edu.ru/auth/login'
    data = {'login': login, 'password': password, "submit": "submit", "returnTo": "https://one.43edu.ru"}
    session.post(url, data=data)

    return session

def get_guid(session: requests.Session) -> str:  # dict
    """
    Получает id пользователя

    :param session: Сессия пользователя
    :return: dict: {name: guid}
    """
    response = session.get("https://one.43edu.ru/edv/index/participant/", verify=False)
    soup = BeautifulSoup(response.text, 'lxml')

    one_participant = soup.find("div", {"class": "one-participant"})
    participants = soup.find("ul", {"id": "participants"})

    if one_participant:
        guid_element = soup.find("div", {"id": "participant"})
        name = one_participant.text.replace("\n", "").strip()
        while "  " in name:
            name = name.replace("  ", " ")
        return guid_element.attrs["data-guid"]  # {name: guid_element.attrs["data-guid"]}
    elif participants:
        guids = {}
        for i in participants.findAll("a"):
            name = " ".join([j.text for j in i.find("div")]).replace("\n", "").strip()
            while "  " in name:
                name = name.replace("  ", " ")
            guids[name] = i.attrs["data-guid"]
        return guids
    return {}