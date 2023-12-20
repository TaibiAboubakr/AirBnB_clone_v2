#!/usr/bin/python3
""" Review module for the HBNB project """
from os import getenv
from models.base_model import BaseModel
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship



class Review(BaseModel):
    """ Review class to store review information """
    if getenv("HBNB_TYPE_STORAGE") == "db":
        __tablename__ = "reviews"
    place_id = ""
    user_id = ""
    text = ""
