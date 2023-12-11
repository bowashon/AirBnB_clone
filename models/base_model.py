#!/usr/bin/python3
"""class representation of the base model"""
import uuid
from datetime import datetime


class BaseModel:
    """
    class BaseModel that defines all common attributes/
    methods for other classes
    """
    def __init__(self):
        """
        Instantiate all attributes
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """
        update public instance attribute with current
        datetime
        """
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """
        Returns dictionary containing all keys/values
        of __dict__ of the instance
        """
        obj_dict = self.__dict__
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
