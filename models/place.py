#!/usr/bin/python3
"""The Place Module"""
from models.base_model import BaseModel


class Place(BaseModel):
    """
    class place that represents an object place
    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = int(0)
    number_bathrooms = int(0)
    max_guest = int(0)
    price_by_night = int(0)
    latitude = float(0.0)
    longitude = float(0.0)
    amenity_id = [""]
