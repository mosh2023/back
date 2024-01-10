

# Project launch

1. Add files .env

## Mock
1. Dependency installation`pip install -r requirements.dev.txt`
2. Starting a web server: `python cli.py auth` `python cli.py game` from directory `./auth_service` `./game_service`
## API with database 
1. Execute the command `docker-compose up --build -d` from directory `./auth_service` `./game_service` 
2. Execute the command `alembic upgrade head` from directory `../app` - table migration
