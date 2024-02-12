

# Project launch

1. Преименовать .env.example в .env

## Prod
1. Прописать команду `docker-compose up --build -d`
### PostgreSQL миграции

### MinIO

## Mock
1. Dependency installation`pip install -r requirements.txt`
2. Start a web server: `python cli.py game`
3. Start a dev web server: `python cli.py game --reload`
## API with database 
1. Execute the command `docker-compose up --build -d` 
2. Execute the command `alembic upgrade head` from directory `./app` - table migration
