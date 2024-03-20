#!/usr/bin/python3
"""This module defines a class to manage sqldb storage for hbnb clone
"""
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
import os


class DBStorage:
    """DBStorage class"""
    __engine = None
    __session = None
    __envs = {
        'env': os.getenv('HBNB_ENV'),
        'user': os.getenv('HBNB_MYSQL_USER'),
        'password': os.getenv('HBNB_MYSQL_PWD'),
        'host': os.getenv('HBNB_MYSQL_HOST'),
        'database': os.getenv('HBNB_MYSQL_DB')
        }

    def __init__(self):
        """instantiates new DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(DBStorage.__envs['user'],
                                              DBStorage.__envs['password'],
                                              DBStorage.__envs['host'],
                                              DBStorage.__envs['database']),
                                      pool_pre_ping=True)

    def all(self, cls=None):
        """queries on the current database session (self.__session) all
        objectsdepending of the class name"""
        sess_objs = {}
        classes = {"State": State, "City": City, "User": User,
                   "Place": Place, "Review": Review, "Amenity": Amenity}
        if cls:
            if type(cls) == str and cls in classes:
                for obj in self.__session.query(classes[cls]).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    sess_objs[key] = obj
            elif cls.__name__ in classes:
                for obj in self.__session.query(cls).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    sess_objs[key] = obj

        else:
            for key, value in classes.items():
                for obj in self.__session.query(value).all():
                    key = str(value.__name__) + "." + str(obj.id)
                    sess_objs[key] = obj

        return sess_objs

    def new(self, obj):
        """adds the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads the DBStorage"""
        Base.metadata.create_all(self.__engine)

        session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session)

        self.__session = Session()

    def close(self):
        """
        closes the session after it's complete
        """
        self.__session.close()
        self.reload()
