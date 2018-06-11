import unittest

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from generator import Generator
from objects.parts import Base


class TestShips(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///ships.sqlite')
        Base.metadata.create_all(self.engine)
        connection = self.engine.connect
        gen = Generator(self.engine)
        gen.initialize()

    def tearDown(self):
        meta = MetaData(self.engine)
        for table in meta.sorted_tables:
            table.drop(self.engine)

    def test_table(self):
        assert True
        "test ..."
