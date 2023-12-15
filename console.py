#!/usr/bin/python3
"""
The console or user interface of the program
"""
import cmd


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

    def emptyline(self, arg):
        """
        executes nothing
        """
        pass

    def do_help(self, arg):
        """
        type help <topic> to get help on the topic
        """
        return super().do_help(arg)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
