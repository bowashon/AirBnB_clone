#!/usr/bin/pyton3
"""The Review module"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    class Review that represents an instance of review
    """
    place_id = ""
    user_id = ""
    text = ""
