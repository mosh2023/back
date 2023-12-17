"""
https://github.com/starlite-api/pydantic-factories
https://lyz-code.github.io/blue-book/coding/python/faker/
https://lyz-code.github.io/blue-book/coding/python/factoryboy/

from typing import Any

from faker import Faker
from faker_optional import OptionalProvider
from pydantic_factories import ModelFactory
from pydantic_factories import Use
import factory

from tests.factories.common import AsyncSQLAlchemyFactory

# Пример фабрик для моделей:

faker.add_provider(OptionalProvider)

class Foo(BaseModel):
    int_value: int
    optional_str: Optional[str]

class FooFactory(ModelFactory[Any]):
    __model__ = Foo

    int_value = Use(faker.pyint)
    optional_str = Use(faker.optional_sentence, nb_words=3, variable_nb_words=True)

FooFactory.build()

# Пример фабрик для таблиц:

class FooORMFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = FooORM
        sqlalchemy_session_persistence = "commit"

    id = factory.Faker("pyint", max_value=1000)

FooORMFactory.create(session)
FooORMFactory.create_batch(session, 3)
"""

from typing import Any
from typing import Generic
from typing import ParamSpec

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
import factory


faker = Faker("ru_RU")

P = ParamSpec("P")


class BoundFactoryMethod(Generic[P]):
    __self__: "AsyncSQLAlchemyFactory"

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Any:
        ...


class AsyncSQLAlchemyFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @staticmethod
    def _execute_cls_method(
        session: AsyncSession, fn: BoundFactoryMethod[P], *args, **kwargs
    ):
        setattr(fn.__self__._meta, "sqlalchemy_session", session)
        return fn(*args, **kwargs)

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        return await session.run_sync(cls._execute_cls_method, super().create, **kwargs)

    @classmethod
    async def create_batch(cls, session: AsyncSession, size, **kwargs):
        return [await cls.create(session, **kwargs) for _ in range(size)]
