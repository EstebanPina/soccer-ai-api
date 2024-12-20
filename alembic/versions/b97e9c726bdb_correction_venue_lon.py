"""Correction Venue Lon

Revision ID: b97e9c726bdb
Revises: c61d8fcc101a
Create Date: 2024-12-05 22:16:40.095429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b97e9c726bdb'
down_revision: Union[str, None] = 'c61d8fcc101a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('SoccerMatches', sa.Column('venueId', sa.String(), nullable=False))
    op.create_foreign_key(None, 'SoccerMatches', 'Venue', ['venueId'], ['id'])
    op.add_column('Venue', sa.Column('weather', sa.String(), nullable=True))
    op.add_column('Venue', sa.Column('temperature', sa.Double(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'temperature')
    op.drop_column('Venue', 'weather')
    op.drop_constraint(None, 'SoccerMatches', type_='foreignkey')
    op.drop_column('SoccerMatches', 'venueId')
    # ### end Alembic commands ###
