"""Se actualizo el HistorialUsuario

Revision ID: cdf9df5fb2d7
Revises: 1e74e8055ca2
Create Date: 2020-06-17 00:24:30.902072

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdf9df5fb2d7'
down_revision = '1e74e8055ca2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('historial_cancion', 'fecha_de_reproduccion',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('historial_cancion', 'fecha_de_reproduccion',
               existing_type=sa.DATE(),
               nullable=False)
    # ### end Alembic commands ###
