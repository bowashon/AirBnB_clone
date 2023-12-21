#!/usr/bin/python3
"""
file storage: serialization and deserialization of files
"""
from models.base_model import BaseModel
import json
import os
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage():
    """
    class FileStorage for serializating and deserializing
    files for storage
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns the dictionary __objects
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>,id
        """
        obj_name = obj.__class__.__name__
        cls_name = "{}.{}".format(obj_name, obj.id)
        FileStorage.__objects[cls_name] = obj

    def save(self):
        """
        serializes __objects to the JSON file
        """
        obj_dict = {}
        for key, value in FileStorage.__objects.items():
            obj_dict[key] = value.to_dict()

        with open(FileStorage.__file_path, 'w') as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        deserilizes the JSON file to __objects
        """
        if not os.path.exists(FileStorage.__file_path):
         return

        deserialized_file = None

        with open(FileStorage.__file_path, 'r') as f:

            try:
                deserialized_file = json.load(f)
            except json.JSONDecodeError:
                pass

            if deserialized_file is None:
                return

            for key, value in deserialized_file.items():
                obj_name, obj_id = key.split('.')
                my_obj = eval(obj_name)
                cls_instance = my_obj(**value)
                FileStorage.__objects[key] = cls_instance
