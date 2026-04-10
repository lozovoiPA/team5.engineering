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

    def execute_query(self, query, use_context_manager=True):
        result = None
        if use_context_manager:
            with sessionmaker(bind=self.engine).begin() as session:
                result = query(session)
        else:

            Session = sessionmaker(bind=self.engine)
            session = Session()
            try:
                result = query(session)
            except Exception as e:
                print(f"Exception in db:\n{e}")
                Session.close_all()
            if session.is_active:
                session.close()
        return result
