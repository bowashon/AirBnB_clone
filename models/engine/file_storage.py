#!/usr/bin/python3
"""
saving data to file
"""
import json
import os


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
        all_obj = FileStorage.__objects
        for key in all_obj.keys():
            obj_dict[key] = all_obj[key].to_dict()

        with open(FileStorage.__file_path, 'w') as file:
            json.dump(obj_dict, file)
            print(f"Saved objects: {obj_dict}")

    def reload(self):
        """
        deserialize the JSON file to __objects
        """
        if os.path.isfile(FileStorage.__file_path):
            with open(FileStorage.__file_path, 'r') as file:
                try:
                    obj_dict = json.load(file)
                    for key, value in obj_dict.items():
                        class_name, class_id = key.split('.')
                        cls = eval(class_name)
                        obj_instance = cls(**value)
                        self.new(obj_instance)
                except FileNotFoundError:
                    pass
