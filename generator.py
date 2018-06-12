import random

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from objects.parts import Hull, Engine, Weapon, Ship

__weapons_names__ = {"Mark {:d}",
                     "Model {:d}",
                     "CM-{:d}",
                     "AK-{:d}"
                     }

__engines_names__ = {"General LM {:d}",
                     "6 ЧН {:d}",
                     "RTA{:d}"
                     }
__ships_names__ = {"Миноносец тип {:d}",
                   "CC-{:d}",
                   "Крейсер проекта {:d}",
                   "HMS  {:d}"
                   }


class Generator:

    def __init__(self) -> None:
        self.used = set()

    def create_ship(self, session):
        ship = self._gen_name(__ships_names__)
        weapon = session.query(Weapon.weapon).order_by(func.random()).first().weapon
        engine = session.query(Engine.engine).order_by(func.random()).first().engine
        hull = session.query(Hull.hull).order_by(func.random()).first().hull
        return Ship(ship=ship, weapon=weapon, hull=hull, engine=engine)

    def _gen_name(self, names_list):
        used = True
        while used:
            new_name = random.choice(list(names_list)).format(random.randint(10, 3000))
            if new_name not in self.used:
                used = False
        self.used.add(new_name)
        return new_name

    def create_hull(self):
        random.seed()
        hull = self._gen_name(["Корпус {:d}"])
        armor = random.randint(100, 500)
        type = random.randint(1, 5)
        capacity = random.randint(1, 10) * armor * type
        return Hull(hull=hull, armor=armor, type=type, capacity=capacity)

    def create_engine(self):
        random.seed()
        engine = self._gen_name(__engines_names__)
        type = random.randint(1, 3)
        power = random.randint(3000, 10000) * type
        return Engine(engine=engine, power=power, type=type)

    def create_weapon(self):
        random.seed()
        weapon = self._gen_name(__weapons_names__)
        reload_speed = random.randint(10, 100)
        rotation_speed = random.randint(5, 20)
        diameter = random.randint(70, 500)
        power_volley = random.randint(20, 500)
        count = random.randint(1, 10)
        return Weapon(weapon=weapon, reload_speed=reload_speed, rotation_speed=rotation_speed, diameter=diameter,
                      power_volley=power_volley, count=count)


class Randomizer:
    def __init__(self, engine):
        self.session = sessionmaker(bind=engine)
        self.gen = Generator()

    def _add(self, session, objects):
        session.add_all(objects)
        session.commit()
        self.gen.used = set()

    def initialize(self):
        session = self.session()
        engines = [self.gen.create_engine() for x in range(6)]
        self._add(session, engines)
        weapons = [self.gen.create_weapon() for x in range(20)]
        self._add(session, weapons)
        hulls = [self.gen.create_hull() for x in range(5)]
        self._add(session, hulls)
        ships = [self.gen.create_ship(session) for x in range(200)]
        self._add(session, ships)
        session.close()

    def randomize(self):
        session = self.session()
        self.rand_element(session, Hull, self.gen.create_hull)
        self.rand_element(session, Weapon, self.gen.create_weapon)
        self.rand_element(session, Engine, self.gen.create_engine)
        self.rand_element(session, Ship, self.gen.create_ship, value=True)
        session.close()

    def rand_element(self, session, table, method, value=False):
        for i in session.query(table):
            if value:
                self.randomize_item(i, method(session))
            else:
                self.randomize_item(i, method())
        session.commit()

    def _rbool(self):
        return bool(random.getrandbits(1))

    def randomize_item(self, item, another):
        randomize = self._rbool()
        if randomize:
            for element in item.variables():
                if self._rbool():
                    setattr(item, element, getattr(another, element))
        return item
