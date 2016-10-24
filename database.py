"""
Create the database schemas for both player and common monsters,
initialize the database by connecting to it, and creating the tables

SQLite
"""
from peewee import *

db = SqliteDatabase("combat_database.db")


class Players(Model):
    """ORM for players table"""
    player_name = CharField(max_length=100)
    hp = IntegerField()
    ac = IntegerField()

    class Meta:
        database = db


class Monsters(Model):
    """ORM for monster table"""
    monster_name = CharField(max_length=100)
    hp = IntegerField()
    ac = IntegerField()
    exp = IntegerField()
    init_mod = IntegerField()
    special = BooleanField()

    class Meta:
        database = db


def initialize_db():
    """Initialize the DB by connecting and creating the tables.
    If the tables are already created, use the existing tables.
    """
    db.connect()
    db.create_tables([Players], safe=True)
    db.create_tables([Monsters], safe=True)
