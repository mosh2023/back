class ORMObjectExistsError(BaseException):
    def __init__(self, cls, id, *args: object) -> None:
        super().__init__(f'{cls} with id={id} does not exist.', *args)
