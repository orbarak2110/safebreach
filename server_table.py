from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///./servers.db") # path to db file


class ServerTable(Base):
    __tablename__ = "server_table" # name of the table
    id = Column(Integer, primary_key=True) # id of the rows in the db(by request you will receive a list[dict] without the id)
    client_ip = Column(String)
    server_id = Column(String)
    request_count = Column(Integer)


Base.metadata.create_all(engine)
