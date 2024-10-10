"""Add table cities

Revision ID: 4fae0d17d8f9
Revises: 
Create Date: 2024-10-08 11:45:22.590824

"""
from typing import Sequence, Union

import geoalchemy2
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4fae0d17d8f9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.create_table('cities',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False, unique=True),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('geom', geoalchemy2.types.Geometry(geometry_type='POINT', srid=4326, from_text='ST_GeomFromEWKT', name='geometry', nullable=False), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    # Создание индекса для geom, если он не существует
    op.execute("CREATE INDEX IF NOT EXISTS idx_cities_geom ON cities USING gist (geom);")
    op.create_index(op.f('ix_cities_id'), 'cities', ['id'], unique=True)
    op.create_index(op.f('ix_cities_name'), 'cities', ['name'], unique=True)

def downgrade() -> None:
    op.drop_index(op.f('ix_cities_id'), table_name='cities')
    op.drop_index(op.f('ix_cities_name'), table_name='cities')
    op.drop_index('idx_cities_geom', table_name='cities', postgresql_using='gist')
    op.drop_table('cities')

