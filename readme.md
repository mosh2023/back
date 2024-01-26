

# Project launch

1. Add files .env

## Mock
1. Dependency installation`pip install -r requirements.dev.txt`
2. Start a web server: `python cli.py game`
3. Start a dev web server: `python cli.py game --reload`
## API with database 
1. Execute the command `docker-compose up --build -d` 
2. Execute the command `alembic upgrade head` from directory `./app` - table migration
