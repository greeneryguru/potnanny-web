from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('login', VARCHAR(length=64)),
    Column('password', VARCHAR(length=255), nullable=False),
    Column('is_active', BOOLEAN, nullable=False),
    Column('name', VARCHAR(length=50)),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('password', String(length=255), nullable=False),
    Column('is_active', Boolean, nullable=False),
    Column('name', Unicode(length=50)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['login'].drop()
    post_meta.tables['users'].columns['username'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['users'].columns['login'].create()
    post_meta.tables['users'].columns['username'].drop()
