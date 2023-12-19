#!/usr/bin/python3
"""new engine DBStorage"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import base_model


class DBStorage:
    """a DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """initializing DBStorage"""
        MySQL_user = getenv("HBNB_MYSQL_USER")
        MySQL_pwd = getenv("HBNB_MYSQL_PWD")
        MySQL_host = getenv("HBNB_MYSQL_HOST", default="localhost")
        MySQL_db = getenv("HBNB_MYSQL_DB")
        MySQL_env = getenv("HBNB_ENV")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MySQL_user, MySQL_pwd, MySQL_host, MySQL_db),
                                      pool_pre_ping=True)
        if MySQL_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        from models import storage
        classes = ["User", "State", "City", "Amenity", "Place", "Review"]
        objs = {}
        if cls:
            class_name = cls.__name__
            objs = {f"{class_name}.{obj.id}": obj
                    for obj in self.__session.query(cls).all()}
        else:
            for class_name in classes:
                class_objects = self.__session.query(eval(class_name)).all()
                objs.update({obj.__class__.__name__ + '.' + obj.id: obj
                             for obj in class_objects})
        return objs
    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and
    create the current database session"""
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))
        base_model.Base.metadata.create_all(self.__engine)

