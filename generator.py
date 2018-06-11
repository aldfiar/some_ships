import random

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

    def __init__(self, engine) -> None:
        self.used = set()
        self.engine = engine

    def initialize(self):
        self.engine.connection()
        Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        engines = [self.create_engine() for x in range(6)]
        self._add(Session, engines)

        weapons = [self.create_weapon() for x in range(20)]
        self._add(Session, weapons)

        hulls = [self.create_hull() for x in range(5)]
        self._add(Session, hulls)

        ships = [
            self.create_ship(random.choice(weapons).weapon,
                             random.choice(engines).engine,
                             random.choice(hulls).hull)
            for x in range(200)]
        self._add(Session, ships)

    def _add(self, session, objects):
        session = session()
        session.add_all(objects)
        session.commit()
        session.close()
        self.used = set()

    def create_ship(self, weapon, engine, hull):
        ship = self._gen_name(__ships_names__)
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
