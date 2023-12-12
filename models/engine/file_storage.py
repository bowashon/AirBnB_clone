#!/usr/bin/python3
"""
Storage engine of all files
"""
import json
from models.base_model import BaseModel


class FileStorage:
    """
    class File storage that serializes instances to JSON file
    and deserializes JSON file back to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        returns the dictionary __object
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        obj_name = obj.__class__.__name__
        key = "{}.{}".format(obj_name, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        serializes __objects to JSON file
        """
        o_dict = {}
        for key, value in FileStorage.__objects.items():
            o_dict[key] = value.to_dict()

        with open(FileStorage.__file_path, 'w') as f:
            json.dump(o_dict, f)

    def reload(self):
        """
        Deserializes the JSON file to __object
        """
        try:
            with open(FileStorage.__file_path, 'r') as f:
                loaded_object = json.load(f)
                for key, value in loaded_object.items():
                    cls_name, obj_id = key.split('.')
                    cls = eval(cls_name)
                    self.new(cls(**value))
        except FileNotFoundError:
            return
