import unittest
from shutil import copyfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from generator import Randomizer
from objects.parts import Base


class TestShips(unittest.TestCase):

    def setUp(self):
        db_file = "ships.sqlite"
        backup_file = "ships_before.sqlite"
        self.engine = create_engine('sqlite:///{}'.format(db_file))
        Base.metadata.create_all(self.engine)
        randomizer = Randomizer(self.engine)
        randomizer.initialize()
        copyfile(db_file, backup_file)
        randomizer.randomize()
        self.unchanged_engine = create_engine('sqlite:///{}'.format(backup_file))
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.Session_unchanged = sessionmaker(bind=self.unchanged_engine, expire_on_commit=False)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_weapons(self):
        pass

    def test_engines(self):
        pass

    def test_hulls(self):
        pass

    def test_ships(self):
        pass

    def check_weapon(self, session):
        pass

    def check_engine(self, engine):
        pass

    def check_hull(self, hull):
        pass

    def check_ship(self, ship):
        pass
