from sqlalchemy import create_engine, Column, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class database(object):
    def setup_database():
        Base.metadata.create_all(self.engine)

    def __init__(self, connection_str):
        self.engine = create_engine(connection_string)
        Session = sessionmaker(self.engine)
        self.session = Session()


class food_events(Base):
    __tablename__ = "food_events"

    id = Column(BigInteger, primary_key=True)
    has_food = Column(Boolean)

    def update_food(self, value):
        self.has_food = value
        self.session.commit()
