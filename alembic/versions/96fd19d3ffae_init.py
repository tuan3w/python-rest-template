"""init

Revision ID: 96fd19d3ffae
Revises:
Create Date: 2022-05-14 20:27:49.273970

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = '96fd19d3ffae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False),
        sa.Column('password', sa.String),
    )
    op.create_table(
        'threads',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('name', sa.String)
    )
    op.create_table(
        'thread_members',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('thread_id', sa.Integer, sa.ForeignKey("threads.id")),
        sa.Column('role', sa.String)
    )
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('thread_id', sa.Integer, sa.ForeignKey("threads.id")),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey("users.id")),
        sa.Column('message', sa.String),
    )p


def downgrade():
    op.drop_table('users')
    op.drop_table('threads')
    op.drop_table('thread_members')
    op.drop_table('messages')
