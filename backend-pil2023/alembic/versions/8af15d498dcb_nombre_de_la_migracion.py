"""Nombre_de_la_migracion

Revision ID: 8af15d498dcb
Revises:
Create Date: 2023-09-29 13:47:35.082301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision: str = '8af15d498dcb'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('barrio', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('barrio', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('barrio', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('campus', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('campus', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('campus', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('carrera', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('carrera', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('carrera', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('ciudad', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('ciudad', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('ciudad', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('facultad', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('facultad', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('facultad', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('genero', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('genero', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('genero', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('lugar', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('lugar', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('lugar', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('pais', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('pais', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('pais', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('personas', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('personas', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('personas', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('personasCarreras', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('personasCarreras', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('personasCarreras', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('programa', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('programa', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('programa', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('provincia', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('provincia', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('provincia', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('tipopersona', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('tipopersona', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('tipopersona', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('universidad', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('universidad', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('universidad', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    op.add_column('usuarios', sa.Column('fecha_alta', sa.DateTime(),server_default=text('CURRENT_TIMESTAMP'), nullable=True))
    op.add_column('usuarios', sa.Column('fecha_modificacion', sa.DateTime(), nullable=True))
    op.add_column('usuarios', sa.Column('activo', sa.Boolean(), server_default=sa.sql.true(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('usuarios', 'activo')
    op.drop_column('usuarios', 'fecha_modificacion')
    op.drop_column('usuarios', 'fecha_alta')
    op.drop_column('universidad', 'activo')
    op.drop_column('universidad', 'fecha_modificacion')
    op.drop_column('universidad', 'fecha_alta')
    op.drop_column('tipopersona', 'activo')
    op.drop_column('tipopersona', 'fecha_modificacion')
    op.drop_column('tipopersona', 'fecha_alta')
    op.drop_column('provincia', 'activo')
    op.drop_column('provincia', 'fecha_modificacion')
    op.drop_column('provincia', 'fecha_alta')
    op.drop_column('programa', 'activo')
    op.drop_column('programa', 'fecha_modificacion')
    op.drop_column('programa', 'fecha_alta')
    op.drop_column('personasCarreras', 'activo')
    op.drop_column('personasCarreras', 'fecha_modificacion')
    op.drop_column('personasCarreras', 'fecha_alta')
    op.drop_column('personas', 'activo')
    op.drop_column('personas', 'fecha_modificacion')
    op.drop_column('personas', 'fecha_alta')
    op.drop_column('pais', 'activo')
    op.drop_column('pais', 'fecha_modificacion')
    op.drop_column('pais', 'fecha_alta')
    op.drop_column('lugar', 'activo')
    op.drop_column('lugar', 'fecha_modificacion')
    op.drop_column('lugar', 'fecha_alta')
    op.drop_column('genero', 'activo')
    op.drop_column('genero', 'fecha_modificacion')
    op.drop_column('genero', 'fecha_alta')
    op.drop_column('facultad', 'activo')
    op.drop_column('facultad', 'fecha_modificacion')
    op.drop_column('facultad', 'fecha_alta')
    op.drop_column('ciudad', 'activo')
    op.drop_column('ciudad', 'fecha_modificacion')
    op.drop_column('ciudad', 'fecha_alta')
    op.drop_column('carrera', 'activo')
    op.drop_column('carrera', 'fecha_modificacion')
    op.drop_column('carrera', 'fecha_alta')
    op.drop_column('campus', 'activo')
    op.drop_column('campus', 'fecha_modificacion')
    op.drop_column('campus', 'fecha_alta')
    op.drop_column('barrio', 'activo')
    op.drop_column('barrio', 'fecha_modificacion')
    op.drop_column('barrio', 'fecha_alta')
    # ### end Alembic commands ###