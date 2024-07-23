![](https://img.shields.io/github/license/Malins062/evtc-telegram-bot)
[<img src="https://img.shields.io/badge/Telegram-%40EVTC_bot-blue">](https://t.me/EVTC_bot)
![](https://img.shields.io/badge/version-2.0.1%20-brightgreen)
![Lint and types](https://github.com/Malins062/evtc-telegram-bot/actions/workflows/lint_and_types.yml/badge.svg?branch=dev)
![Build and publish](https://github.com/Malins062/evtc-telegram-bot/actions/workflows/publish.yml/badge.svg?branch=main)
![](https://img.shields.io/github/forks/Malins062/evtc-telegram-bot)

# Эвакуация ТС (телеграмм-бот) ![Логотип](.github/images/bot_icon.png) 

Бот предназначен для передачи информации об эвакуированных транспортных средствах, посредствам электронной почты.

![Фото](https://user-images.githubusercontent.com/Malins062/evtc-telegram-bot/.github/images/bot_description_picture.png)

## Технологии

* [Aiogram](https://github.com/aiogram/aiogram) — работа с Telegram Bot API;
* [Redis](https://redis.io) — персистентное хранение данных (персистентность включается отдельно);
* [Docker](https://www.docker.com) и [Docker-Compose](https://docs.docker.com/compose) — быстрое разворачивание бота в изолированном контейнере.

## Установка

Скопируйте файл `.env.example` как `.env` (с точкой в начале), откройте и отредактируйте содержимое. Создайте каталоги 
`redis_data` и `redis_config`, в последний подложите свой конфиг `redis.conf` 
(в репозитории есть [пример](redis.conf)).

Наконец, запустите бота командой `docker-compose up -d`. 
