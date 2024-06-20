## Деплой бота на сервере

Протестировано на Debian 10.

Обновляем систему

```bash
sudo apt update && sudo apt upgrade
```

Устанавливаем Python 3.10 сборкой из исходников и sqlite3:

```bash
cd
sudo apt install -y sqlite3 pkg-config
wget https://www.python.org/ftp/python/3.10.11/Python-3.10.11.tgz
tar -xzvf Python-3.10.11.tgz
cd Python-3.11.1
./configure --enable-optimizations --prefix=/home/www/.python3.10
sudo make altinstall
```

Устанавливаем Poetry:

```basj
curl -sSL https://install.python-poetry.org | python3 -
```

Клонируем репозиторий в `~/code/evtc_bot`:

```bash
mkdir -p ~/code/
cd ~/code
git clone https://github.com/Malins062/evtc-telegram-bot.git
cd evtc-bot
```

Создаём переменные окружения:

```
cp evtc_bot/.env.example evtc_bot/.env
vim evtc_bot/.env
```

`TELEGRAM_BOT_TOKEN` — токен бота, полученный в BotFather, `TELEGRAM_evtc_CHANNEL_ID` — идентификатор группы книжного клуба, участие в котором будет проверять бот в процессе голосования.

Заполняем БД начальными данными:

```bash
cat evtc_bot/db.sql | sqlite3 evtc_bot/db.sqlite3
```

Устанавливаем зависимости Poetry и запускаем бота вручную:

```bash
poetry install
poetry run python -m evtc_bot
```

Можно проверить работу бота. Для остановки, жмём `CTRL`+`C`.

Получим текущий адрес до Pytnon-интерпретатора в poetry виртуальном окружении Poetry:

```bash
poetry shell
which python
```

Скопируем путь до интерпретатора Python в виртуальном окружении.

Настроим systemd-юнит для автоматического запуска бота, подставив скопированный путь в ExecStart, а также убедившись,
что директория до проекта (в данном случае `/home/www/code/evtc_bot`) у вас такая же:

```
sudo tee /etc/systemd/system/evtcbot.service << END
[Unit]
Description=evtc Telegram bot
After=network.target

[Service]
User=www
Group=www-data
WorkingDirectory=/home/www/code/evtc-bot
Restart=on-failure
RestartSec=2s
ExecStart=/home/www/.cache/pypoetry/virtualenvs/evtc-bot-dRxws4wE-py3.11/bin/python -m evtc_bot

[Install]
WantedBy=multi-user.target
END

sudo systemctl daemon-reload
sudo systemctl enable evtcbot.service
sudo systemctl start evtcbot.service
```