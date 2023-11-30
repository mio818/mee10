from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
import abc
from sqlalchemy.orm import sessionmaker, Session, scoped_session


engine = create_engine("mysql://root:TpHSWotUTKhL22@db:3306/happyDB")
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_discord_id: int = Column(BigInteger, primary_key=True)
    user_name: String = Column(String(255))
    created_at = Column(DateTime, default=DateTime)
    updated_at = Column(DateTime, default=DateTime)
    deleted_at = Column(DateTime, default=DateTime)

    def exists_or_create(self) -> bool:
        SessionClass = sessionmaker(engine)
        session = SessionClass()
        user = session.query(User).filter(User.user_discord_id == self.user_discord_id).first()
        if not user:
            session.add(self)
            session.commit()
        return user


# class UserRepository(abc.ABC):
#     @abc.abstractmethod
#     def find_user_by_id(self, user_id: int) -> User:
#         raise NotImplementedError

#     @abc.abstractmethod
#     def save(self, user: User) -> User:
#         raise NotImplementedError


# class UserRepositoryImpl(UserRepository):
#     def __init__(self):
#         SessionClass = sessionmaker(engine)
#         self.session = SessionClass()


#     def find_user_by_id(self, user_id: int) -> User:
#         user = self.session.query(User).filter(User.user_discord_id == user_id).first()
#         # userが存在しない場合は作成する

#         return


class Point(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    point = Column(BigInteger, default=0, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
    user_id = Column(BigInteger, ForeignKey("users.user_discord_id"))


class PointRepository(abc.ABC):
    @abc.abstractmethod
    def add_20_point(self, user: User) -> Point:
        raise NotImplementedError

    @abc.abstractmethod
    def get_point(self, user_id: int) -> Point:
        raise NotImplementedError


class PointRepositoryImpl(PointRepository):
    def __init__(self):
        SessionClass = sessionmaker(engine)
        self.session = SessionClass()

    def add_20_point(self, user: User) -> Point:
        point = self.session.query(Point).filter(Point.user_id == user.user_discord_id).first()
        point.point += 20
        self.session.commit()
        return point

    def get_point(self, user: User) -> Point:
        pass


Base.metadata.create_all(engine)
