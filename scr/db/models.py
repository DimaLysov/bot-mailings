from sqlalchemy import BigInteger, String, ForeignKey, Column, Integer, LargeBinary, Text, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from scr.config import DATABASE_URL

engine = create_async_engine(url=DATABASE_URL)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(BigInteger, unique=True)


class UserEmails(Base):
    __tablename__ = 'Users_Emails'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    email = Column(String)
    password = Column(String)
    status = Column(Boolean, default=False)


class Sample(Base):
    __tablename__ = 'Samples'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    theme = Column(String)
    text_name = Column(Text, default=None)
    photo_name = Column(Text, default=None)
    status = Column(Boolean, default=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print('database is active')
