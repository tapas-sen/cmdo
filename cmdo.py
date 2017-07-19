#!/usr/bin/python
import sys
import argparse
import os

import display
import dal


class TodoList:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='')

        self.dal = dal.DAL()

        self.display = display.Display()

        self.parser.add_argument('-l', '--list', help="", action="store_true")
        self.parser.add_argument('-a', '--add', help="", type=str, nargs="+")
        self.parser.add_argument('--due', help="", type=str)
        self.parser.add_argument('-r', '--remove', help="", type=int)
        self.parser.add_argument('-d', '--done', help="", type=int)
        self.parser.add_argument('--undone', help="", type=int)  # Revert done
        self.parser.add_argument('-v', '--view', help="", type=int)
        self.parser.add_argument('-t', '--debug', help="",  action="store_true")
        self.parser.add_argument('--description', help="", nargs="*")
        self.parser.add_argument('--vacuum', help="", action="store_true")

        args = self.parser.parse_args()

        if self.check_arguments(args):
            self.handle_arguments(args)
        else:
            self.display.clear_terminal()
            self.display.display_welcome()

        self.dal.close_connection()
        self.reset_terminal()

    def check_arguments(self, args):
        any_arg_set = False
        for arg in vars(args):
            if getattr(args, arg):
                any_arg_set = True
                break
        return any_arg_set


    def handle_arguments(self, args):
        display_list = False
        # TODO - Display list is happening too many times here, it could be called multiple times depending on the operation

        if args.add:
            # TODO - Should handle description here as well
            due_date = None
            if args.due:
                due_date = args.due
            self.dal.add_to_cmdo_list(args.add, due_date)
            display_list = True
        if args.description and not args.add:
            # Split the args into the id and description
            self.dal.add_description(args.description[0], args.description[1::])
        if args.remove:
            self.dal.remove_by_id(args.remove)
            display_list = True

        if args.done:
            self.dal.mark_as_done(args.done)
            display_list = True
        if args.undone:
            self.dal.mark_as_undone(args.undone)
            display_list = True

        if args.debug:
            self.dal.dump_database()
        if args.vacuum:
            self.dal.vacuum_id()
            display_list = True
        if args.view:
            self.display_details(args.view)

        if args.list or display_list:
            self.display_list()

    def display_details(self, item_id):
        self.display.display_details(self.dal.get_item_description(item_id))

    def display_list(self):
        cmdo_list = self.dal.get_cmdo_list()
        self.display.show_list(cmdo_list)

    def reset_terminal(self):
        # TODO - Check if this works on unix
        os.system('color')

td_list = TodoList()


