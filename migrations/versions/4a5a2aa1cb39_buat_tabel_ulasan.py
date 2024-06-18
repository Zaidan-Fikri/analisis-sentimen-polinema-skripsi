"""buat tabel ulasan

Revision ID: 4a5a2aa1cb39
Revises: fddb20c60b18
Create Date: 2024-06-03 04:37:56.895190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a5a2aa1cb39'
down_revision = 'fddb20c60b18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ulasan',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ulasan', sa.String(length=255), nullable=False),
    sa.Column('label', sa.String(length=255), nullable=True),
    sa.Column('predicted_label', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ulasan')
    # ### end Alembic commands ###