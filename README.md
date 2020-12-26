<<<<<<< HEAD
# Telegram-бот
Обращаясь к API Яндекс.Практикума бот присылает сообщения при изменении статуса домашнего задания.

###Как развернуть проект локально

1. Склонируйте репозиторий

```git clone <ссылка на репозиторий> <название локальной папки>```

2. Создайте и активируйте виртуальное окружение

```python -m venv venv && . venv\scripts\activate```

3. Установите необходимые пакеты

```pip install -r requirements.txt```

4. Создайте бота в Телеграм (он будет присылать вам сообщения): Найдите @BotFather,нажмите Start и выполните команду /newbot. Задайте имя и техническое имя вашего бота. После создания бота вы получите токен TELEGRAM_TOKEN.

5. В директории проекта нужно создать файл .env с личными данными:

    PRAKTIKUM_TOKEN='' - можно получить по ссылке https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a.

    TELEGRAM_TOKEN='' - получен на предыдущем шаге.

    TELEGRAM_CHAT_ID='' - можно узнать, обратившись к @getmyid_bot

6. Запустить бота

```python homework.py```
=======

My telegram bot for checking the homework status in Yandex.Practicum
>>>>>>> e5772360b4fcc397506ae344bf60d70a9a6777ce
