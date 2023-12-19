#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models import base_model  # Assuming there is a 'base' module where your models are defined



class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if cls is None:
            return FileStorage.__objects
        else:
            if not isinstance(cls, type):
                raise TypeError("cls must be a class")
            filtered_objects = {k: v for k, v in FileStorage.__objects.items()
                                if isinstance(v, cls)}
            return filtered_objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ delete obj from __objects if it’s inside """
        if obj:
            className = obj.__class__.__name__
            delobj = f"{className}.{obj.id}"
            del self.__objects[delobj]

class DBStorage:
    """ New engine fo MySQL storage """
    __engine=None
    __session=None
    
    def __init__(self):
        """ Initialization method """
        db_url = 'mysql+mysqldb://hbnb_dev:hbnb_dev_pwd@localhost:3306/hbnb_dev_db'
        db_url1 = f"mysql+mysqldb://{os.environ['HBNB_MYSQL_USER']}:{os.environ['HBNB_MYSQL_PWD']}@{os.environ['HBNB_MYSQL_HOST']}:3306/{os.environ['HBNB_MYSQL_DB']}"
        self.__engine = create_engine(db_url, pool_pre_ping=True)
        
        if os.environ.get('HBNB_ENV') == 'test':
            self.__engine.execute("DROP TABLE IF EXISTS cities, amenities, users, places, reviews, states;")
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def all(self, cls=None):
        """Query on the current database session"""

        objects = {}
        classes = [base_model.User, base_model.State, base_model.City, base_model.Amenity, base_model.Place, base_model.Review]

        if cls is not None:
            classes = [cls]

        for model_class in classes:
            query_result = self.__session.query(model_class).all()
            for obj in query_result:
                key = f"{obj.__class__.__name__}.{obj.id}"
                objects[key] = obj
        return objects
    def new(self, obj):
        """ add the object to the current database session """
        self.__session.add(obj)
        
    def save(self):
        """ commit all changes of the current database session """
        self.__session.commit()
        
    def delete(self, obj=None): 
        """  delete from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current database session"""
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        base_model.Base.metadata.create_all(self.__engine)
