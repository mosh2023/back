"""add auth table

Revision ID: 3bb4dda18d50
Revises: 63d662fbc764
Create Date: 2024-01-13 18:00:28.929407

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bb4dda18d50'
down_revision = '41f1af9febcf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
    CREATE TABLE auth (
        id SERIAL PRIMARY KEY NOT NULL,
        login VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(128) NOT NULL,
        role auth_role NOT NULL
    );
    
    CREATE TYPE auth_role AS ENUM ('user', 'admin');

    CREATE TABLE "user" (
        id serial4 NOT NULL,
        auth_id int4 NOT NULL,
        name varchar(50) NOT NULL,
        icon_link text NULL,
        UNIQUE (auth_id),
        PRIMARY KEY (id)
    );
    
    CREATE TABLE player (
        id serial4 NOT NULL,
        user_id int4 NULL,
        remaining_moves int4 NOT NULL,
        used_moves int4 NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (user_id) REFERENCES "user" (id)
    );
    
    CREATE TABLE prize (
        id serial4 NOT NULL,
        "name" varchar(50) NOT NULL,
        description text NULL,
        icon_link text NULL,
        admin_id int4 NOT NULL,
        dt_won timestamp NULL,
        user_id int4 NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (admin_id) REFERENCES "user" (id),
        FOREIGN KEY (user_id) REFERENCES "user" (id)
    );
    
    CREATE TABLE boat (
        id serial4 NOT NULL,
        prize_id int4 NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (prize_id) REFERENCES prize (id)
    );
    
    CREATE TABLE game (
        id serial4 NOT NULL,
        "name" varchar(50) NOT NULL,
        description text NULL,
        board_size int4 NOT NULL,
        "key" varchar(10) NOT NULL,
        admin_id int4 NOT NULL,
        dt_start timestamp NULL,
        player1_id int4 NULL,
        player2_id int4 NULL,
        UNIQUE ("key"),
        PRIMARY KEY (id),
        FOREIGN KEY (admin_id) REFERENCES "user" (id),
        FOREIGN KEY (player1_id) REFERENCES player (id),
        FOREIGN KEY (player2_id) REFERENCES player (id)
    );


    CREATE TABLE field (
        id serial4 NOT NULL,
        game_id int4 NOT NULL,
        x int4 NOT NULL,
        y int4 NOT NULL,
        injured bool NOT NULL,
        boat_id int4 NULL,
        player_id int4 NULL,
        PRIMARY KEY (id),
        FOREIGN KEY (boat_id) REFERENCES boat (id),
        FOREIGN KEY (game_id) REFERENCES game (id),
        FOREIGN KEY (player_id) REFERENCES player (id)
    );
    """)


def downgrade() -> None:
    pass
