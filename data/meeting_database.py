from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

base = declarative_base()


class MeetingDb(base):
    __tablename__ = 'meetings'
    id: int = Column(Integer, primary_key=True)
    name: str = Column(String)
    timestamp: datetime = Column(DateTime)
    description: str = Column(String)
    priority: bool = Column(Boolean)


class MeetingDatabase:
    def __init__(self, path):
        self.engine = create_engine(f'sqlite:///{path}')
        base.metadata.create_all(self.engine)

    def execute_query(self, query):
        result = None
        with sessionmaker(bind=self.engine).begin() as session:
            result = query(session)
        return result
