"""auth_service

Revision ID: 1a53114626ec
Revises: 
Create Date: 2023-12-27 14:06:11.823417

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a53114626ec'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE TABLE auth (
        id SERIAL PRIMARY KEY NOT NULL,
        login VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(128) NOT NULL,
        is_admin BOOLEAN NOT NULL
    );
    """)


def downgrade():
    op.execute("""
    DROP TABLE auth;
    """)
