#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models
from models.city import City


class State(BaseModel, Base):
    """a state class that inherits from BaseModel"""
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", back_populates="states",
                              cascade="all , delete")
    else:
        name = ""

        @property
        def get_cities(self):
            """getter that returns the cities with state_id"""
            from models import storage
            city_instname = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    city_instname.append(city)
            return city_instname
