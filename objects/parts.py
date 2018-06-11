from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Hull(Base):
    __tablename__ = "hulls"
    hull = Column(String(250), primary_key=True)
    armor = Column(Integer)
    type = Column(Integer)
    capacity = Column(Integer)


class Weapon(Base):
    __tablename__ = "weapons"
    weapon = Column(String(250), primary_key=True)
    reload_speed = Column(Integer)
    rotation_speed = Column(Integer)
    diameter = Column(Integer)
    power_volley = Column(Integer)
    count = Column(Integer)


class Engine(Base):
    __tablename__ = "engines"
    engine = Column(String(250), primary_key=True)
    power = Column(Integer)
    type = Column(Integer)


class Ship(Base):
    __tablename__ = "ships"
    ship = Column(String(250), primary_key=True)
    weapon = Column(String(250), ForeignKey('weapons.weapon'))
    hull = Column(String(250), ForeignKey('hulls.hull'))
    engine = Column(String(250), ForeignKey('engines.engine'))
