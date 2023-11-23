from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger


engine = create_engine("mysql://root:TpHSWotUTKhL22@db:3306/happyDB")
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_discord_id: int = Column(BigInteger, primary_key=True)
    user_name: String = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)


class Point(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    point = Column(BigInteger, default=0, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user_id = Column(BigInteger, ForeignKey("users.user_discord_id"))


Base.metadata.create_all(engine)
