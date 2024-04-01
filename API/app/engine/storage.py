from app.config import DBConfig, classes
from sqlalchemy import create_engine
from app.models import Base
from sqlalchemy.orm import scoped_session, sessionmaker
from app.utils.helper import set_dict
import os

class DBStorage:
    """The storage configuration class."""

    __engine = None
    __session = None

    def __init__(self) -> None:
        if os.getenv("DB") == "REMOTE":
            DB_NAME = os.getenv("DB_NAME")
            USER_NAME = os.getenv("USER_NAME")
            PASSWORD = os.getenv("PASSWORD")
            HOST = os.getenv("HOST")
            self.__engine = create_engine(f"mysql+mysqlconnector://{USER_NAME}:{PASSWORD}@{HOST}:3306/{DB_NAME}")
        else:
            self.__engine = create_engine(DBConfig().url)

    @property
    def session(self):
        """A getter for the session attribute."""
        return self.__session

    def new(self, obj):
        """A method that adds a new object."""
        self.__session.add(obj)

    def save(self):
        """A method that saves the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """A method that deletes the current object."""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """A method that reloads from the database."""
        Base.metadata.create_all(self.__engine)
        session_maker = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_maker)

    def close(self):
        """A method that closes the database session."""
        self.__session.close()

    def drop(self):
        """A method that drops the data of the database."""
        Base.metadata.drop_all(self.__engine)

    def get(self, cls=None, **kwargs):
        """A method that returns a object based on the class name and the id."""
        data = {}
        if not kwargs:
            if cls is None:
                for val in classes.values():
                    obj_list = self.__session.query(val).all()
                    set_dict(obj_list, data)
                return data
            obj_list = self.__session.query(classes[cls]).all()
            set_dict(obj_list, data)
            return data
        obj_list = self.__session.query(classes[cls]).filter_by(**kwargs)
        set_dict(obj_list, data)
        return data
