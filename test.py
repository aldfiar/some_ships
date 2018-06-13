from shutil import copyfile

import nose
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from generator import Randomizer
from objects.parts import Base, Weapon, Ship, Engine, Hull

db_file = "ships.sqlite"
backup_file = "ships_before.sqlite"


class TestShips(object):
    @classmethod
    def setupClass(cls):
        cls.engine = create_engine('sqlite:///{}'.format(db_file))
        Base.metadata.create_all(cls.engine)
        randomizer = Randomizer(cls.engine)
        randomizer.initialize()
        copyfile(db_file, backup_file)
        randomizer.randomize()
        cls.unchanged_engine = create_engine('sqlite:///{}'.format(backup_file))
        cls.session = sessionmaker(bind=cls.engine, expire_on_commit=False)
        cls.session_unchanged = sessionmaker(bind=cls.unchanged_engine, expire_on_commit=False)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(cls.engine)

    def test_weapons(self):
        for new in self.session().query(Ship):
            old = self.session_unchanged().query(Ship).get(new.ship)
            yield self.check_ship, new, old, Weapon, "weapon"

    def test_engines(self):
        for new in self.session().query(Ship):
            old = self.session_unchanged().query(Ship).get(new.ship)
            yield self.check_ship, new, old, Engine, "engine"

    def test_hulls(self):
        for new in self.session().query(Ship):
            old = self.session_unchanged().query(Ship).get(new.ship)
            yield self.check_ship, new, old, Hull, "hull"

    def check_ship(self, new, old, parameter, key):
        self.check(Ship, new, old)
        new_param = self.session().query(parameter).get(getattr(new, key))
        old_param = self.session_unchanged().query(parameter).get(getattr(new, key))
        self.check(parameter, new_param, old_param)

    def check(self, table, new, old):
        for element in table.variables():
            new_element = getattr(new, element)
            old_element = getattr(old, element)
            nose.tools.eq_(new_element, old_element,
                           msg="Expected {type} {element}: {old}, was {new}".format(type=table, element=element,
                                                                                    old=old_element, new=new_element))
