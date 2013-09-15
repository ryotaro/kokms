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
    engine = create_engine('sqlite:///' + password, echo=True, encoding="utf-8")
    # Initial table creation.
    KokmsCore.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    current_session = Session()
    return current_session

"""
Enumerate names.
"""
def iterator_name(session):
    # execute sql
    entities = session.query(KokmsCore).group_by(KokmsCore.name)
    # iterate over entity set
    for entity in entities:
        yield entity.name

"""
Enumerate existing dates.
"""
def iterator_existing_dates(session):
    # execute sql
    entities = session.query(KokmsCore).group_by(KokmsCore.date)
    # iterate over entity set
    for entity in entities:
        yield entity.date


"""
Introduce the earliest date among the DB.
"""
def get_mindate(session):
    for entity in session.query(func.min(KokmsCore.date)):
        return entity[0]
    
"""
Introduce the latest date among the DB.
"""
def get_maxdate(session):
    for entity in session.query(func.max(KokmsCore.date)):
        return entity[0]



"""
Close current session and commit.
"""
def close_session():
    current_session.commit()
    
    
    