"""add foreign-key to posts table

Revision ID: 359f02de3c0d
Revises: ee7a7353376e
Create Date: 2022-06-11 06:27:32.158753

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '359f02de3c0d'
down_revision = 'ee7a7353376e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))

    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',
                                           local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
