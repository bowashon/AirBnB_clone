#!/usr/bin/python3
"""class representation of the base model"""
import uuid
import models
from datetime import datetime


class BaseModel:
    """
    class BaseModel that defines all common attributes/
    methods for other classes
    """
    def __init__(self, *args, **kwargs):
        """
        Instantiate all attributes arguments for the constructor of
        a BaseModel
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
        else:
            models.storage.new(self)

    def save(self):
        """
        update public instance attribute with current
        datetime
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        Returns dictionary containing all keys/values
        of __dict__ of the instance
        """
        obj_dict = self.__dict__.copy()
        class_name = self.__class__.__name__
        obj_dict['__class__'] = class_name
        for key, value in obj_dict.items():
            if key in ('created_at', 'updated_at'):
                obj_dict[key] = value.isoformat()

        return (obj_dict)

    def __str__(self):
        """
        Return the object representation for printing
        """
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)
