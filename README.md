[<img src="https://img.shields.io/badge/Telegram-%40EVTC_bot-blue">](https://t.me/EVTC_bot)

# ![Логотип](repo_images/logo.jpg) Эвакуация ТС (telegram-bot)

Бот предназначен для передачи информации об эвакуированных транспортных средствах, посредствам электронной почты.

![Фото](repo_images/bot_description_picture.jpg)

## Технологии

* [Aiogram](https://github.com/aiogram/aiogram) — работа с Telegram Bot API;
* [Redis](https://redis.io) — персистентное хранение данных (персистентность включается отдельно);
* [Docker](https://www.docker.com) и [Docker-Compose](https://docs.docker.com/compose) — быстрое разворачивание бота в изолированном контейнере.

## Установка

Скопируйте файл `.env.example` как `.env` (с точкой в начале), откройте и отредактируйте содержимое. Создайте каталоги 
`redis_data` и `redis_config`, в последний подложите свой конфиг `redis.conf` 
(в репозитории есть [пример](redis.example.conf)).

Наконец, запустите бота командой `docker-compose up -d`. 
