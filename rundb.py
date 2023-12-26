from app.db.tables import *
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

def main():
    engine = sa.create_engine('')
    recreate_db(engine)

    Session = sessionmaker(engine)
    # with Session() as session:
    #     player = PlayerORM(name='Vlad')
    #     session.add(player)
    #     session.commit()

    #     reg = AuthORM(player_id=player.id, login='log123', password='123321v')
    #     session.add(reg)
    #     session.commit()
 

    with Session() as session:
        res = session.scalars(
            sa.select(PlayerORM)).all()
        
        reg = session.scalars(
            sa.select(AuthORM)).all()

    print(res)
    print(reg)


def recreate_db(engine):
    from app.db.tables.base import get_metadata
    meta = get_metadata()
    meta.drop_all(engine)
    meta.create_all(engine)


if __name__ == '__main__':
    main()

