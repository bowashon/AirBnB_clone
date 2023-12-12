#!/usr/bin/python3
"""
command interpreter console module
"""
import cmd


class HBNBCommand(cmd.Cmd):
    """
    class for command interpreter
    """
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """Quit command to exit the program"""

        return True

    def do_EOF(self, arg):
        """
        EOF command to exit the program
        """
        print("")

        return True

    def emptyline(self):
        """
        empty line + ENTER shouldn't execute anything
        """
        pass


if __name__ == "__main__":
    HBNBCommand().cmdloop()
