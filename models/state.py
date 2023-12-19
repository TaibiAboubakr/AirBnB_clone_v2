#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
from models.city import City

class State(BaseModel):
    """a state class that inherits from BaseModel"""
    if getenv ("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state", cascade="all , delete")
    else:
        name = ""

        @property
            def cities(self):
                """getter that returns the cities with state_id"""
                from models import storage
                city_instname = []
                for city in storage.all(City).values():
                    if city.state_id == self.id:
                        city_instname.append(city)
                return city_instname
