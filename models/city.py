#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    name = Column(String(60), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'),
                      ondelete='CASCADE', nullable=False)
    state = relationship('State', back_populates='City')

    state_id = ""
    name = ""
