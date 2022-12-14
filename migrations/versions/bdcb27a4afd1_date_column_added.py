"""Date column added

Revision ID: bdcb27a4afd1
Revises: 1a687013c830
Create Date: 2022-05-27 10:25:04.494818

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bdcb27a4afd1'
down_revision = '1a687013c830'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('date', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'date')
    # ### end Alembic commands ###
