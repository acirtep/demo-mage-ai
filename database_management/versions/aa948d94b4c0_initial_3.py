"""initial 3

Revision ID: aa948d94b4c0
Revises: aa3a8a88650a
Create Date: 2022-11-16 16:16:46.758203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'aa948d94b4c0'
down_revision = 'aa3a8a88650a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('raw_order', sa.Column('cut_off_date', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('raw_order', 'cut_off_date')
    # ### end Alembic commands ###
