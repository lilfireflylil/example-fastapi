"""add foreign-key to posts table

Revision ID: 5a760b805650
Revises: 1e151ee06d3e
Create Date: 2024-06-05 15:38:01.409238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a760b805650'
down_revision: Union[str, None] = '1e151ee06d3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer() ,nullable=False))
    op.create_foreign_key('posts_users_fk', 
                          source_table='posts', referent_table='users',
                          local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
