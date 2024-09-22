"""delete recipient_id to Message model

Revision ID: bf0df8e60fb2
Revises: c7a56509e8b2
Create Date: 2024-09-04 21:47:11.516697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf0df8e60fb2'
down_revision = 'c7a56509e8b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_constraint('messages_recipient_id_fkey', type_='foreignkey')
        batch_op.drop_column('recipient_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(sa.Column('recipient_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('messages_recipient_id_fkey', 'users', ['recipient_id'], ['user_id'])

    # ### end Alembic commands ###
