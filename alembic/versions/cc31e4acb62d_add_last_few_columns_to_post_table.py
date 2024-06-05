"""add last few columns to post table

Revision ID: cc31e4acb62d
Revises: 5a760b805650
Create Date: 2024-06-05 15:58:03.272436

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc31e4acb62d'
down_revision: Union[str, None] = '5a760b805650'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
    
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                            nullable=False))
    
    # the below code work the same as above
    ''' 

    op.add_column('posts', 
                  sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False),
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))

    '''
    pass


def downgrade() -> None:
    op.drop_column(table_name='posts', column_name='published')
    op.drop_column(table_name='posts', column_name='created_at')
    pass
