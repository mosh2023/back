"""create initial tables

Revision ID: 9f5ccb4e753b
Revises: 
Create Date: 2024-02-13 01:23:29.880516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f5ccb4e753b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("""
        CREATE TYPE "roles" AS ENUM ('user', 'admin');
        """)

    op.execute("""
        CREATE TABLE auth (
            id serial4 NOT NULL,
            login varchar(50) NOT NULL,
            "password" varchar(128) NOT NULL,
            "role" "roles" NOT NULL,
            CONSTRAINT auth_login_key UNIQUE (login),
            CONSTRAINT auth_pkey PRIMARY KEY (id)
        );        
        """)

    op.execute("""
        CREATE TABLE "user" (
            id serial4 NOT NULL,
            auth_id int4 NOT NULL,
            "name" varchar(50) NOT NULL,
            icon_link text NULL,
            CONSTRAINT user_auth_id_key UNIQUE (auth_id),
            CONSTRAINT user_pkey PRIMARY KEY (id),
            CONSTRAINT user_auth_id_fkey FOREIGN KEY (auth_id) REFERENCES auth(id)
        );      
        """)

    op.execute("""
        CREATE TABLE player (
            id serial4 NOT NULL,
            user_id int4 NULL,
            remaining_moves int4 NOT NULL,
            used_moves int4 NOT NULL,
            CONSTRAINT player_pkey PRIMARY KEY (id),
            CONSTRAINT player_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id)
        );     
        """)

    op.execute("""
        CREATE TABLE prize (
            id serial4 NOT NULL,
            "name" varchar(50) NOT NULL,
            description text NULL,
            icon_link text NULL,
            admin_id int4 NOT NULL,
            dt_won timestamp NULL,
            user_id int4 NULL,
            CONSTRAINT prize_pkey PRIMARY KEY (id),
            CONSTRAINT prize_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES "user"(id),
            CONSTRAINT prize_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id)
        );
        """)

    op.execute("""
        CREATE TABLE boat (
            id serial4 NOT NULL,
            prize_id int4 NOT NULL,
            CONSTRAINT boat_pkey PRIMARY KEY (id),
            CONSTRAINT boat_prize_id_key UNIQUE (prize_id),
            CONSTRAINT boat_prize_id_fkey FOREIGN KEY (prize_id) REFERENCES prize(id)
        );
        """)

    op.execute("""
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
            CONSTRAINT game_key_key UNIQUE (key),
            CONSTRAINT game_pkey PRIMARY KEY (id),
            CONSTRAINT game_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES "user"(id),
            CONSTRAINT game_player1_id_fkey FOREIGN KEY (player1_id) REFERENCES player(id),
            CONSTRAINT game_player2_id_fkey FOREIGN KEY (player2_id) REFERENCES player(id)
        );
        """)

    op.execute("""
        CREATE TABLE field (
            id serial4 NOT NULL,
            game_id int4 NOT NULL,
            x int4 NOT NULL,
            y int4 NOT NULL,
            injured bool NOT NULL,
            boat_id int4 NULL,
            player_id int4 NULL,
            CONSTRAINT field_boat_id_key UNIQUE (boat_id),
            CONSTRAINT field_pkey PRIMARY KEY (id),
            CONSTRAINT unique_field UNIQUE (game_id, x, y),
            CONSTRAINT field_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES boat(id),
            CONSTRAINT field_game_id_fkey FOREIGN KEY (game_id) REFERENCES game(id),
            CONSTRAINT field_player_id_fkey FOREIGN KEY (player_id) REFERENCES player(id)
        );
        """)


def downgrade() -> None:
    op.execute("DROP TABLE field;")
    op.execute("DROP TABLE game;")
    op.execute("DROP TABLE boat;")
    op.execute("DROP TABLE prize;")
    op.execute("DROP TABLE player;")
    op.execute('DROP TABLE "user";')
    op.execute("DROP TABLE auth;")
    op.execute('DROP TYPE "roles";')


