"""create posts table

Revision ID: ba2734a30549
Revises: 
Create Date: 2024-03-10 10:18:59.444274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba2734a30549'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                            sa.Column('title',sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
