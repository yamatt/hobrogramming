from sqlalchemy import create_engine, Column, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class database(object):
    def setup_database(self):
        Base.metadata.create_all(self.engine)

    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        Session = sessionmaker(self.engine)
        self.session = Session()
        
    def get_event(self, id):
        return self.session.query(food_events).filter_by(id=id).first()
        
    def update_food(self, id, value):
        food_event = self.get_event(id)
        food_event.update_food(value)

class food_events(Base):
    __tablename__ = "food_events"

    id = Column(BigInteger, primary_key=True)
    has_food = Column(Boolean)

    def update_food(self, value):
        self.has_food = value
        self.session.commit()
