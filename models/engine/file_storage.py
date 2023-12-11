#!/usr/bin/python3
"""
saving data to file
"""
import json


class FileStorage:
    """
    class FileStorage that serializes instances to a JSON
    file and deserialize JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the diction __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj
        print(f"Added object: {key}")

    def save(self):
        """
        serialiaze __object to JSON file
        """
        obj_dict = {}
        for key, value in FileStorage.__objects.items():
            obj_dict[key] = value.to_dict()

        with open(FileStorage.__file_path, 'w') as file:
            json.dump(obj_dict, file)
            print(f"Saved objects: {obj_dict}")

    def reload(self):
        """
        deserialize the JSON file to __objects
        """
        try:
            with open(FileStorage.__file_path, 'r') as file:
                obj_instance = json.load(file)
                for key, value in obj_instance.items():
                    cls_name, obj_id = key.split('.')
                    cls = eval(cls_name)
                    obj_instance = cls(**value)
                    self.new(obj)
        except FileNotFoundError:
            pass
