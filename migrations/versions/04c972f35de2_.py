"""empty message

Revision ID: 04c972f35de2
Revises: eecf96691f3b
Create Date: 2020-09-07 23:15:36.065868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04c972f35de2'
down_revision = 'eecf96691f3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('idea', schema=None) as batch_op:
        batch_op.add_column(sa.Column('userteam', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_idea_userteam_user'), 'user', ['userteam'], ['userteam'], ondelete='CASCADE')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('idea', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_idea_userteam_user'), type_='foreignkey')
        batch_op.drop_column('userteam')

    # ### end Alembic commands ###
