from typing import Union
import requests
import xlrd
import pandas as pd
import csv
from datetime import date as d

def get_marks(session: requests.Session, guid: str, begin: str = None, end: str = None,
                  final_grades: bool = False) -> list:
    """
    Получает данные об оценках. Необходимо указать период, либо final_grades=True.
    **Если оценки отсутствуют, будет записано "нет"**

    :param session: Сессия пользователя
    :param guid: Guid пользователя
    :param begin: Начала периода (строка в формате *DD.MM.YYYY*)
    :param end: Конец периода (строка в формате *DD.MM.YYYY*)
    :param final_grades: Итоговые оценки
    """
    if final_grades:
        url = "https://one.43edu.ru/edv/index/report/period/" + guid
        data = {"format": "xls"}
    else:
        url = "https://one.43edu.ru/edv/index/report/marks/" + guid
        data = {"begin": begin, "end": end, "format": "xls"}
    response = session.get(url, params=data, verify=False)
    workbook = xlrd.open_workbook(file_contents=response.content, ignore_workbook_corruption=True)
    df = pd.read_excel(workbook)
    csv_data = df.to_csv(index=False)

    rows = list(csv.reader(csv_data.splitlines()[4:]))

    marks = []
    for row in rows:
        subject = {
            'name': row[1],
            'marks': row[2].split(', '),
            'gpa': row[3],
        }
        marks.append(subject)
        

    return marks