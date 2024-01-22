"""unique_fields

Revision ID: 1b528ebb5f63
Revises: c6e6c458ef3c
Create Date: 2024-01-22 08:46:18.222650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b528ebb5f63'
down_revision = 'c6e6c458ef3c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('unique_field', 'field', ['game_id', 'x', 'y'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_field', 'field', type_='unique')
    # ### end Alembic commands ###
