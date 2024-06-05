"""add user table

Revision ID: 1e151ee06d3e
Revises: d80b69bf05b8
Create Date: 2024-06-05 15:04:15.479357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e151ee06d3e'
down_revision: Union[str, None] = 'd80b69bf05b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                              server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint('id'), # Can also add "primary_key=True" directly in Column "id"
                    sa.UniqueConstraint('email') # Can also add "unique=True" directly in Column "email"
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass


# 10:57:21