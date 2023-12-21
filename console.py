#!/usr/bin/python3
"""
The console or user interface of the program
"""
import cmd
import re
import ast
import shlex
import json
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State


_classes = {
        'BaseModel': BaseModel,
        'User': User,
        'City': City,
        'Place': Place,
        'State': State,
        'Amenity': Amenity,
        'Review': Review,
        }

def parse_update(attr):
        match_str = re.search(r"\{(.*?)\}", attr)
        if match_str:
            class_id = shlex.split(attr[:match_str.span()[0]])
            new_id = [_.strip(',') for _ in class_id][0]
            str_data = match_str.group(1)
            try:
                str_dict = ast.literal_eval("{" + str_data + "}")
            except Exception:
                return
            print(str_dict)
            return new_id, str_dict
        else:
            command = [_.strip() for _ in attr.split(',')]
            try:
                new_id = command[0]
                attr_name = command[1]
                attr_value = command[2]
            except Exception:
                return
            return "{} {} {}".format(new_id, attr_name, attr_value)

class HBNBCommand(cmd.Cmd):
    """
    the HBNBCommand class that defines the entry point
    of the code
    """

    prompt = "(hbnb)"

    def do_quit(self, arg):
        """
        quit command to exit the program
        ***************************
        Usage: quit + enter
        """
        return True

    def do_EOF(self, arg):
        """
        EOF to exit the program
        ************************
        usage: EOF
        """
        print("")
        return True

    def emptyline(self):
        """
        executes nothing
        """
        pass

    def do_help(self, arg):
        """
        type help <topic> to get help on the topic
        """
        return super().do_help(arg)

    def do_create(self, arg):
        """
        creates a new instance of BaseModel, saves it
        to JSON file
        **********************************************
        Usage: create <name>
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")

        elif args[0] not in _classes:
            print("** class doesn't exist **")
        else:
            new_obj = _classes[args[0]]()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, arg):
        """
        prints the string representation of an instance based on
        the class name and id.
        Usage : $ show BaseModel 1234-1234-1234
        """
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in _classes:
            print("** class doesn't exit **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            saved_objs = storage.all()
            key = "{}.{}".format(args[0], args[1])
            obj = saved_objs.get(key, None)
            if obj is None:
                print("** no instance found **")
            else:
                print(obj)

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id
        Usage: destroy BaseModel 1234-1234-1234
        """
        args = shlex.split(arg)

        if not args:
            print("**class name missing **")
        elif args[0] not in _classes:
            print("** class doesn't exit **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(args[0], args[1])
            stored_obj = storage.all()
            obj = stored_obj.get(key, None)
            if obj is not None:
                del stored_obj[key]
                storage.save()
            else:
                print("** no instance found **")
                return

    def do_all(self, arg):
        """
        Prints all string representation of all instances based
        or not on the class name
        Usage: all BaseModel
               $all
        """
        args = shlex.split(arg)
        all_obj = storage.all()

        if not args:
            for key, value in all_obj.items():
                print(["{}".format(str(value))])
            return

        elif args[0] not in _classes:
            print("** class doesn't exist **")
            return
        else:
            for key, value in all_obj.items():
                if key.split('.')[0] == args[0]:
                    print(str(value))
            return

    def do_count(self, arg):
        """
        Count the number of instances created
        """
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
        elif args[0] not in _classes:
            print("** class doesn't exist **")
        else:
            all_objs = storage.all()
            count = 0
            for key in all_objs.keys():
                if key.split('.')[0] == args[0]:
                    count = count + 1
            print(count)

    def do_update(self, arg):
        """
        updates instance based on the class name and id
        by adding or updating attributes
        Usage: <class name> <id> <attributes name> "attribute value>"
        """
        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return
        elif args[0] not in _classes:
            print("** class doesn't exist **")
            return
        elif len(args) < 2:
            print("** instance id missing **")
            return

        all_objs = storage.all()
        key = "{}.{}".format(args[0], args[1])
        obj = all_objs.get(key, None)
        if obj is None:
            print("** no instance found **")
            return

        elif len(args) < 3:
            print("** attribute name missing **")
            return

        elif len(args) < 4:
            print("** value missing **")
            return

        else:
            match_str = re.search(r"\{(.*?)\}", arg)
            if match_str:
                data_str = match_str.group(1)
                str_dict = ast.literal_eval("{" + data_str + "}")
                for key, value in str_dict.items():
                    attr_name = key
                    attr_value = value
                    setattr(obj, attr_name, attr_value)
            else:   
                attr_name = args[2]
                attr_value = shlex.split(args[3])[0]

            if attr_name in ["id", "created_at", "updated_at"]:
                return

            try:
                attr_value = eval(attr_value)
            except Exception:
                pass

            setattr(obj, attr_name, attr_value)
            obj.save()

    def default(self, arg):
        """
        Defines default that over writes the cmd default
        """
        args = arg.split('.')
        class_name = args[0]
        command = args[1].split("(")
        command_method = command[0]
        incoming_id = command[1].split(")")
        class_id = incoming_id[0]

        command_dict = {
                'all': self.do_all,
                'create': self.do_create,
                'show': self.do_show,
                'destroy': self.do_destroy,
                'update': self.do_update,
                'count': self.do_count}
        if command_method in command_dict.keys():
            if command_method == 'update':
                attr = command[1].split(")")
                new_id, class_args = parse_update(attr[0])
                if isinstance(class_args, dict):
                    update_str = " ".join(["{} {}".format(k, v) for k, v in class_args.items()])
                    return_values = command_dict[command_method]("{} {} {}".format(
                                                            class_name, new_id, update_str))
                    return return_values
                elif isinstance(class_args, str):
                    return command_dict[command_method](" {} {} {} {}".format(class_name,
                                                    new_id, attr_name, attr_value))
            else:
                return command_dict[command_method](" {} {}".format(class_name, class_id))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
