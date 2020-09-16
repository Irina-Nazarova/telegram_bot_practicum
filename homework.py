import os
import requests
import telegram
import time
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(filename)s - %(message)s",
)

PRACTICUM_TOKEN = os.getenv("PRACTICUM_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

URL = "https://praktikum.yandex.ru/api/user_api/homework_statuses/"
BOT = telegram.Bot(token=TELEGRAM_TOKEN)


def parse_homework_status(homework):
    """
    Формируем сообщение из JSON полученного из API Яндекс Практикум:
    {'id': 43314,
    'status': 'approved',
    'homework_name': 'Irina-Nazarova__api_01_sms.zip',
    'reviewer_comment': '',
    'date_updated': '2020-09-09T18:35:16Z',
    'lesson_name': 'Отправка SMS-уведомлений'}
    """
    if ("status") not in homework:
        logging.error("Внешний сервис сейчас недоступен")
        return f"Внешний сервис сейчас недоступен"
    verdicts = {
        "rejected": "К сожалению в работе нашлись ошибки.",
        "approved": "Ревьюеру всё понравилось, можно приступать к следующему уроку.",
    }
    homework_name = homework.get("homework_name")
    if homework.get("status") == "rejected":
        return (
            f'У вас проверили работу "{homework_name}"'
            + verdicts[homework.get("status")]
        )
    elif homework.get("status") == "approved":
        return (
            f'У вас проверили работу "{homework_name}"'
            + verdicts[homework.get("status")]
        )
    logging.error("Возникла ошибка с получением данных о статусе работы")
    return f"Возникла ошибка с получением данных о статусе работы"


def get_homework_statuses(current_timestamp):
    """
    Обращается к API Яндекс Практикум и получает статус домашней работы.
    """
    if current_timestamp is None:
        logging.error("Возникла ошибка с форматом даты")
        return {}
    params = {"from_date": current_timestamp}
    headers = {"Authorization": f"OAuth {PRACTICUM_TOKEN}"}
    try:
        homework_statuses = requests.get(URL, headers=headers, params=params)
        return homework_statuses.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка соединения: {e}")


def send_message(message):
    """
    Обращается к API Telegram и отправляет сообщение боту.
    """
    return BOT.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())  # начальное значение timestamp
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            # Пользователь авторизован или нет
            if new_homework.get("code") == "not_authenticated":
                logging.error(
                    "API Yandex Practice token authentication filed."
                )
            elif new_homework.get("homeworks"):
                send_message(
                    parse_homework_status(new_homework.get("homeworks")[0])
                )
            current_timestamp = new_homework.get(
                "current_date"
            )  # обновить timestamp

            time.sleep(1200)  # опрашивать раз в 20 минут

        except Exception as e:
            logging.error(f"Бот упал с ошибкой: {e}")
            time.sleep(5)
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        logging.error(f"You went out!{e}")
