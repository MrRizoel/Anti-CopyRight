
import sqlalchemy
from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DB_URL = ""

def start() -> scoped_session:
    engine = sqlalchemy.create_engine(DB_URL, client_encoding="utf8")
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

class Channels(BASE):
    __tablename__ = "channels"
    __table_args__ = {'extend_existing': True}
    chat_id = Column(BigInteger, primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(BigInteger, primary_key=True)

    def __init__(self, user_id):
        self.user_id = user_id

Users.__table__.create(checkfirst=True)
Channels.__table__.create(checkfirst=True)


def adduser(user_id):
   Check = SESSION.query(Users).get(int(user_id))
   if not Check:
      SESSION.add(Users(user_id))
      SESSION.commit()
   else:
      SESSION.close()

def addchat(chat_id):
   Check = SESSION.query(Channels).get(int(chat_id))
   if not Check:
      SESSION.add(Channels(chat_id))
      SESSION.commit()
   else:
      SESSION.close()
