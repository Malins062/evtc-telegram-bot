[<img src="https://img.shields.io/badge/Telegram-%40EVTC_bot-blue">](https://t.me/EVTC_bot)
![Lint and types](https://github.com/Malins062/evtc-telegram-bot/actions/workflows/lint_and_types.yml/badge.svg?branch=dev)
![Build and publish](https://github.com/Malins062/evtc-telegram-bot/actions/workflows/publish.yml/badge.svg?branch=main)

# ![Логотип](repo_images/bot_icon.png) Эвакуация ТС (telegram-bot)

Бот предназначен для передачи информации об эвакуированных транспортных средствах, посредствам электронной почты.

![Фото](repo_images/bot_description_picture.png)

## Технологии

* [Aiogram](https://github.com/aiogram/aiogram) — работа с Telegram Bot API;
* [Redis](https://redis.io) — персистентное хранение данных (персистентность включается отдельно);
* [Docker](https://www.docker.com) и [Docker-Compose](https://docs.docker.com/compose) — быстрое разворачивание бота в изолированном контейнере.

## Установка

Скопируйте файл `.env.example` как `.env` (с точкой в начале), откройте и отредактируйте содержимое. Создайте каталоги 
`redis_data` и `redis_config`, в последний подложите свой конфиг `redis.conf` 
(в репозитории есть [пример](redis.conf)).

Наконец, запустите бота командой `docker-compose up -d`. 
