"""add content column to posts table

Revision ID: d80b69bf05b8
Revises: f2962f02e4aa
Create Date: 2024-06-05 14:16:37.135925

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd80b69bf05b8'
down_revision: Union[str, None] = 'f2962f02e4aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
