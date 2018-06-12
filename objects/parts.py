from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vars:
    items = []

    @classmethod
    def variables(cls):
        return cls.items


class Hull(Base, Vars):
    items = ["armor", "type", "capacity"]
    __tablename__ = "hulls"
    hull = Column(String(250), primary_key=True)
    armor = Column(Integer)
    type = Column(Integer)
    capacity = Column(Integer)


class Weapon(Base, Vars):
    items = ["reload_speed", "rotation_speed", "power_volley", "count"]
    __tablename__ = "weapons"
    weapon = Column(String(250), primary_key=True)
    reload_speed = Column(Integer)
    rotation_speed = Column(Integer)
    diameter = Column(Integer)
    power_volley = Column(Integer)
    count = Column(Integer)


class Engine(Base, Vars):
    items = ["power", "type"]
    __tablename__ = "engines"
    engine = Column(String(250), primary_key=True)
    power = Column(Integer)
    type = Column(Integer)


class Ship(Base, Vars):
    items = ["weapon", "hull", "engine"]
    __tablename__ = "ships"
    ship = Column(String(250), primary_key=True)
    weapon = Column(String(250), ForeignKey('weapons.weapon'))
    hull = Column(String(250), ForeignKey('hulls.hull'))
    engine = Column(String(250), ForeignKey('engines.engine'))
