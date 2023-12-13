#!/usr/bin/python3
"""
command interpreter console module
"""
import cmd
from models.base_model import BaseModel
from models import storage
import re


def split(s):
    return s.split()


def pars(arg):
    """
    Search for rectangle or curly brace in string
    using regular expressions
    """
    brac = re.search(r"\[(.*?)\]", arg)
    brace = re.search(r"\{(.*?)\}", arg)
    parentheses = re.search(r"\((.*?)\)", arg)
    if brace is None:
        if brac is None:
            if parentheses is None:
                return [text.strip(",") for text in split(arg)]
            else:
                para = split(arg[:parentheses.span()[0]])
                ret_line = [text.strip(",") for text in para]
                ret_line.append(parenthesis.group())
                return ret_line
        else:
            para = split(arg[:brac.span()[0]])
            ret_line = [text.strip(",") for text in para]
            ret_line.append(brac.group())
    else:
        para = split(arg[:brace.span()[0]])
        ret_line = [text.strip(",") for text in para]
        ret_line.append(brace.group())
        return ret_line


class HBNBCommand(cmd.Cmd):
    """
    class for command interpreter
    """
    prompt = "(hbnb) "

    __classes = {
            "User",
            "BaseModel",
            "Place",
            "State",
            "City",
            "Amenity",
            "Review"
            }

    def do_quit(self, arg):
        """Quit command to exit the program"""

        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program
        """
        print("")

        return True

    def do_create(self, arg):
        """
        Create a new class instance and print its id
        """
        my_arg = pars(arg)
        if not my_arg:
            print("** class name missing **")
        elif my_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(my_arg[0])()
            storage.save()
            print(new_instance.id)

    def do_show(self, arg):
        """
        Print string representation of an instance based on
        class name and id
        """
        my_arg = pars(arg)
        obj_dict = storage.all()
        if len(my_arg) == 0:
            print("** class name missing **")
        elif my_arg[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(my_arg) == 1:
            print("** instance id missing **")
        else:
            instance_key = "{}.{}".format(my_arg[0], my_arg[1])
            if instance_key not in obj_dict:
                print("** no instance found **")
            else:
                print(obj_dict[instance_key])

    def do_destroy(self, arg):
        """
        Delete an instance based on class name and id
        """
        my_arg = pars(arg)
        obj_dict = storage.all()
        if not my_arg:
            print("** class name missing **")
        elif my_arg[0] not in  HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(my_arg) < 2:
            print("** instance id missing **")
        else:
            instance_key = "{}.{}".format(my_arg[0], my_arg[1])
            if instance_key not in obj_dict:
                print("** no instance found **")
            else:
                del obj_dict[instance_key]
                storage.save()

    def do_all(self, arg):
        """
        Print string representation of all instances based on
        the class name
        """
        my_arg = pars(arg)
        obj_dict = storage.all()
        if not my_arg or my_arg[0] not in  HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            result_list = [str(obj) for key, obj in obj_dict.items() if
                           key.startswith(my_arg[0] + ".")]
            print(result_list)

    def do_count(self, arg):
        """
        Retrieve the number of instances of a given class.
        """
        args = pars(arg)
        count = 0
        for obj in storage.all().values():
            if args[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """
        Update an instance based on class name and id
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        my_arg = pars(arg)
        obj_dict = storage.all()
        if not my_arg:
            print("** class name missing **")
        elif my_arg[0] not in  HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(my_arg) < 2:
            print("** instance id missing **")
        elif len(my_arg) < 3:
            print("** attribute name missing **")
        elif len(my_arg) < 4:
            print("** value missing **")
        else:
            instance_key = "{}.{}".format(my_arg[0], my_arg[1])
            if instance_key not in obj_dict:
                print("** no instance found **")
            else:
                obj = obj_dict[instance_key]
                attr_name = my_arg[2]
                attr_value = my_arg[3]

                if hasattr(obj, attr_name):
                    setattr(obj, attr_name, type(getattr(obj,
                                                 attr_name))(attr_value))
                    storage.save()
                else:
                    print("** attribute doesn't exist **")

    def emptyline(self):
        """
        empty line + ENTER shouldn't execute anything
        """
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
