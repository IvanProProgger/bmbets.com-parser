import sys

import requests
from bs4 import BeautifulSoup

PARSE_URL = "https://bmbets.com/"


def get_parse_link() -> str:
    """
    Запрашивает у пользователя название категории, региона и лиги.

    Возвращает ссылку на соответствующую страницу
    """
    category = input("Введите вид спорта:\n")
    region = input("Введите регион:\n")
    division = input("Введите дивизион:\n")
    if not all([category, region, division]):
        sys.exit("Введена некорректная информация")

    parse_link = PARSE_URL + "/".join(
        map(
            lambda x: x.replace(" ", "-").lower(), [category, region, division]
        )
    )

    return parse_link


def parse_matches_for_coefs(response) -> None:
    """
    Получает ответ от сервера. Парсит матчи и соответсвующие коэффициенты.
    Вывод в консоль результат
    """
    soup = BeautifulSoup(response.text, "html.parser")
    participants = []
    coeffs = []
    participants_coeffs = []
    for link in soup.find_all("td", class_="players-name-col"):
        participants.append(link.text.strip().replace("\n\n\n\n", " vs "))
    if participants:
        if soup.find_all("td", class_="odds-col4") != []:
            for link in soup.find_all("td", class_="odds-col4"):  # TODO может быть odds-col3
                coeffs.append(link.text.strip().replace("B's", " ")[1:])
        else:
            for link in soup.find_all("td", class_="odds-col3"):
                coeffs.append(link.text.strip().replace("B's", " ")[1:])
    count = len(coeffs) // len(participants)  # TODO Всегда ли в одном спорте, лиге... одинаковое кол-во кэфов
    while len(coeffs) > 0:
        participants_coeffs.append(", ".join(coeffs[:count]))
        coeffs = coeffs[count:]
    parsed_data = zip(participants, participants_coeffs)
    for element in parsed_data:
        print(*element)


if __name__ == "__main__":
    parse_link = get_parse_link()
    try:
        response = requests.get(parse_link, timeout=60)
    except requests.exceptions.Timeout:
        print("Время ожидания истекло")
    except requests.exceptions.RequestException:
        print("Ошибка обработки запроса")
    parsed_data = parse_matches_for_coefs(response)