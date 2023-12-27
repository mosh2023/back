

# Запуск проекта

1. Добавить файлы .env
2. Выполнить команду `docker-compose up --build -d` из директории `./auth_service` `./game_service` 
3. Выполнить команду `alembic upgrade head` из директории `../app` - создание таблиц в бд
4. Запуск веб-сервера: `python cli.py auth` `python cli.py game` из директории `./auth_service` `./game_service`
