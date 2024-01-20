class ORMObjectNoFoundError(BaseException):
    '''ORM object with specified `id` does not exist.'''
    def __init__(self, cls: str, id: int, *args: object) -> None:
        '''ORM object with specified `id` does not exist.'''
        super().__init__(f'{cls} with id={id} does not exist.', *args)


class ORMUniqueFieldError(BaseException):
    '''One of the fields does not match the uniqueness property.'''
    def __init__(self, orm, *args: object) -> None:
        '''One of the fields does not match the uniqueness property.'''
        super().__init__(f'One of the fields of {orm} does not match the uniqueness property.', *args)


class ORMIdIsRequiredError(BaseException):
    '''For executing certain operation value of `id` field is required.'''
    def __init__(self, *args: object) -> None:
        '''For executing certain operation value of `id` field is required.'''
        super().__init__('To execute this operation value of `id` field is required.' *args)


class ORMNoFieldsToUpdateError(BaseException):
    '''There is no fields to update. You should set one of the optional parameters.'''
    def __init__(self, cls: str, id: int, *args: object) -> None:
        '''There is no fields to update. You should set one of the optional parameters.'''
        super().__init__(f'There is no fields to update for `{cls}` with id={id}. You should set one of the optional parameters.', *args)
