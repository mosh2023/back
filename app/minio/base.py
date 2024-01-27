from app.core import config
from app.models.api import Id


class BaseMinio:
    CLS_NAME = 'base'
    PATH = CLS_NAME + '/{id}/{field}'
    URL = config.MINIO_URL

    def __init__(self, obj: Id) -> None:
        self.id = obj.id

    # Насчет расширений файлов: можешь добавлять это через PATH в дочерних классах
    def get_url(self, field: str) -> str:
        return self.URL + self.PATH.format(id=self.id, field=field)

    # можно передавать field в init, как удобнее
    async def upload(self, field: str, file) -> str:
        ...
        return self.get_url(field)

    async def rewrite(self, field: str, file) -> str:
        ...
        return self.get_url(field)

    async def download(self, field: str) -> bytes:
        # not bytes actualy.
        ...
