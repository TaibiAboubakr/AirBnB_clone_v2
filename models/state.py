#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
rom sqlalchemy import Column, String, ForeignKey
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
