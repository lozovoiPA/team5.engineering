from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

base = declarative_base()


class MeetingDb(base):
    __tablename__ = 'meetings'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    time = Column(String)
    date = Column(String)
    description = Column(String)
    priority = Column(Boolean)


class MeetingDatabase:
    def __init__(self, path):
        self.engine = create_engine(f'sqlite:///{path}')
        base.metadata.create_all(self.engine)

    def execute_query(self, query):
        result = None
        with sessionmaker(bind=self.engine).begin() as session:
            result = query(session)
        return result
