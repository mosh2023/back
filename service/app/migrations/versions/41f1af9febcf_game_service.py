"""game_service

Revision ID: 41f1af9febcf
Revises: 
Create Date: 2023-12-26 23:05:34.652937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41f1af9febcf'
down_revision = '63d662fbc764'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE player (
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(50) NOT NULL,
        icon_link TEXT
    );

    CREATE TABLE game (
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(50) NOT NULL,
        description TEXT,
        board_size INT NOT NULL,
        key VARCHAR(10) UNIQUE NOT NULL,
        player1_id INT,
        player1_remaining_moves INT,
        player1_used_moves INT,
        player2_id INT,
        player2_remaining_moves INT,
        player2_used_moves INT,
        admin_id INT NOT NULL,
        datetime_start TIMESTAMP,
        datetime_end TIMESTAMP,
        CONSTRAINT game_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES player(id),
        CONSTRAINT game_player1_id_fkey FOREIGN KEY (player1_id) REFERENCES player(id),
        CONSTRAINT game_player2_id_fkey FOREIGN KEY (player2_id) REFERENCES player(id)
    );

    CREATE TABLE prize (
        id SERIAL PRIMARY KEY NOT NULL,
        name VARCHAR(50) NOT NULL,
        description TEXT,
        icon_link TEXT,
        admin_id INT NOT NULL,
        player_id INT,
        datetime TIMESTAMP,
        CONSTRAINT prize_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES player(id),
        CONSTRAINT prize_player_id_fkey FOREIGN KEY (player_id) REFERENCES player(id)
    );

    CREATE TABLE boat (
        id SERIAL PRIMARY KEY NOT NULL,
        prize_id INT NOT NULL,
        CONSTRAINT boat_prize_id_fkey FOREIGN KEY (prize_id) REFERENCES prize(id)
    );

    CREATE TABLE field (
        id SERIAL PRIMARY KEY NOT NULL,
        game_id INT NOT NULL,
        x INT NOT NULL,
        y INT NOT NULL,
        injured BOOLEAN NOT NULL,
        player_id INT,
        boat_id INT,
        CONSTRAINT field_boat_id_fkey FOREIGN KEY (boat_id) REFERENCES boat(id),
        CONSTRAINT field_game_id_fkey FOREIGN KEY (game_id) REFERENCES game(id),
        CONSTRAINT field_player_id_fkey FOREIGN KEY (player_id) REFERENCES player(id)
    );
    """)

def downgrade():
    op.execute("""
    DROP TABLE field;
    DROP TABLE boat;
    DROP TABLE prize;
    DROP TABLE game;
    DROP TABLE player;
    """)