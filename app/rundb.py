from db.tables import *
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

def main():
    engine = sa.create_engine('')
    Session = sessionmaker(engine)
    with Session() as session:
        res = session.scalars(
            sa.select(PlayerORM))
    print(res)


if __name__ == '__main__':
    main()


# from db.tables.base import get_metadata
# meta = get_metadata()
# meta.create_all(engine)
