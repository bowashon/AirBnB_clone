#!/usr/bin/python3
"""class representation of the base model"""
import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    Defines a class BaseModel as base mode for all instances
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize BaseModel instance
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key in ['created_at', 'updated_at']:
                        value = datetime.fromisoformat(value)
                    setattr(self, key, value)
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updatad_at' not in kwargs:
                self.updated_at = datetime.now()
            
            storage.new(self)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            updated_at = datetime.now()

    def __str__(self):
        """
        returns the rectangle to be printed
        """
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)

    def save(self):
        """
        update public instance attribute with current datetime
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
        returns a dictionary containing all keys/values
        """
        cls_name = self.__class__.__name__
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = cls_name

        for key, value in obj_dict.items():
            if isinstance(value, datetime):
                obj_dict[key] = value.isoformat()

        return (obj_dict)
