# !coding:utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()
class KokmsCore(Base):
    __tablename__ = "kokms_core"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    stat = Column(String)
    name = Column(String)
    mins = Column(Integer)
    
    def __init__(self, date, time, stat, name, mins):
        self.date = date
        self.time = time
        self.stat = stat
        self.name = name
        self.mins = mins
        
"""
Create session by given password.
"""
def open_session(password):
    global current_session
    engine = create_engine('sqlite:///' + password, echo=True)
    # Initial table creation.
    KokmsCore.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    current_session = Session()
    return current_session

"""
Close current session and commit.
"""
def close_session():
    current_session.commit()
    