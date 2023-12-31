#!/usr/bin/python3
"""
BaseModel module
"""
import models
import uuid
from datetime import datetime


class BaseModel():
    """
    class BaseModel as a base model for all classes
    """
    def __init__(self, *args, **kwargs):
        """
        instantiate the class BaseModel
        """
        t_fmt = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid.uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        self.__dict__[key] = datetime.strptime(value, t_fmt)
                    else:
                        self.__dict__[key] = value
        models.storage.new(self)

    def __str__(self):
        """
        return the string representation for
        """
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)

    def save(self):
        """
        updates the public instance attribute updated_at with
        datetime
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        returns dictionary representation of the class
        """
        my_dict = self.__dict__.copy()
        cls_name = self.__class__.__name__
        my_dict['__class__'] = cls_name
        for key, value in my_dict.items():
            if key in ('created_at', 'updated_at'):
                my_dict[key] = value.isoformat()
        return my_dict
