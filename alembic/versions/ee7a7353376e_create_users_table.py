"""create users table

Revision ID: ee7a7353376e
Revises: 6ca7adefbf27
Create Date: 2022-06-11 06:19:46.880688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee7a7353376e'
down_revision = '6ca7adefbf27'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",sa.Column('id',sa.Integer(),nullable=False),
                            sa.Column('email',sa.String(),nullable=False),
                            sa.Column('password',sa.String(),nullable=False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
                            sa.UniqueConstraint('email'),
                            sa.PrimaryKeyConstraint('id')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
