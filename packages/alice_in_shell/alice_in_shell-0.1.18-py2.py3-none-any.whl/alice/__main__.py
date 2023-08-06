#!/usr/bin/env python3

# -*- coding: utf-8 -*-

"""Execute main and secondary menu"""

__version__ = "0.1.18"

import os
import re
import curses
from curses import textpad
from collections import OrderedDict
from math import ceil


import subprocess

# import alice.menu as menu_list

# from alice.config import HOME, EDITOR
# from alice_in_shell import Alice_in_shell as wonderland


# User home dir
HOME = os.path.expanduser("~")

# By default is system editor. You can define your prefered editor as Sublime, VS Code etc.

EDITOR = os.environ.get("EDITOR") if os.environ.get("EDITOR") else "vim"
# EDITOR = "subl"
# EDITOR = "code"


MAIN_MENU = ["Edit alias list", "Choose alias", "Exit"]



class Alice_in_shell:
    def __init__(self, home):
        # shell & aliases file path
        self.home = home
        self.config_path = f'{self.home}/.{str(os.environ["SHELL"][9:])}_aliases'

    def get_aliases(self):
        aliases = OrderedDict()
        mode = "r" if os.path.exists(self.config_path) else "a+"
        try:
            with open(self.config_path, mode) as f:
                for line in f.readlines():
                    clean = line.replace('"', "")
                    result = re.split(r"=", clean)
                    name = result[0].replace("alias", "").lstrip()
                    cmd = result[1].rstrip()
                    aliases[name] = cmd
            return aliases
        except Exception as e:
            raise e

    def source_aliases(self):
        try:
            cmd = f'source {self.home}/.{str(os.environ["SHELL"][9:])}rc'
            subprocess.call([os.environ["SHELL"], "-ic", cmd])
        except Exception as e:
            raise e

    def edit_aleases(self, editor):
        mode = "a"
        try:
            with open(self.config_path, mode):
                subprocess.call([editor, self.config_path])
        except Exception as e:
            raise e

    @staticmethod
    def alias_paginate(ordered, page_counter: int):
        alias_menu_page_counter = page_counter
        pages = int(ceil(len(ordered) / 10))
        if alias_menu_page_counter <= pages:
            count = 0
            chunk = {}
            for key in ordered:
                if count != 0:
                    if (
                        ((alias_menu_page_counter - 1) * 10)
                        < count
                        <= (alias_menu_page_counter * 10)
                    ):
                        chunk[f"{count}. {key}"] = ordered[key]
                elif count == 0 and alias_menu_page_counter == 1:
                    chunk[f"{count}. {key}"] = ordered[key]
                count += 1
            return chunk
        else:
            return 0


class Menu:
    """Generate menu"""

    def __init__(self, menu, height, width):
        self.menu = menu
        self.height = height
        self.width = width

    def get_menu_list(self, stdscr, row_id: int, menu_mode: str):
        stdscr.clear()
        try:
            if menu_mode == "main":
                for _id, row in enumerate(self.menu):
                    x = self.width // 2 - len(row) // 2
                    y = self.height // 2 - len(self.menu) // 2 + _id
                    if _id == row_id:
                        stdscr.addstr(y, x, f"{row}", curses.color_pair(1))
                    else:
                        stdscr.addstr(y, x, f"{row}")

            elif menu_mode == "aliases":
                for _id, row in enumerate(self.menu):
                    alias_body = self.menu[row]
                    if len(alias_body) >= 40:
                        formatted_body = alias_body.split()
                        alias_body = "\n\t".join(formatted_body)
                    x = self.width // 5
                    y = int(self.height // 2.5) - len(self.menu) // 2 + _id
                    if _id == row_id:
                        # draw a container for alias <body> column
                        container = [
                            [1, int(self.width / 2.5)],
                            [self.height - 4, self.width - 3],
                        ]
                        textpad.rectangle(
                            stdscr,
                            container[0][0],
                            container[0][1],
                            container[1][0],
                            container[1][1],
                        )
                        stdscr.setscrreg(0, self.height - 20)

                        stdscr.refresh()
                        stdscr.addstr(y, x - x // 2, row, curses.color_pair(2))
                        for y, line in enumerate(alias_body.splitlines(), 2):
                            stdscr.addstr(y, x + self.width // 4, line, curses.A_DIM)
                    else:
                        stdscr.addstr(y, x - x // 2, row)
            stdscr.refresh()
        except Exception as e:
            if str(e) == "addwstr() returned ERR":
                print("Sorry, screen too small")


alice = Alice_in_shell(HOME)
ALIASES = alice.get_aliases()

def main(stdscr):
    alice.source_aliases()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_BLUE)

    # A UNINTENDED LOL-ZONE: SORRY FOR THIS
    # ------------+----------+-------------
    #      /\O    |    _O    |      O
    #       /\/   |   //|_   |     /_
    #      /\     |    |     |     |\
    #     /  \    |   /|     |    / |
    #   LOL  LOL  |   LLOL   |  LOLLOL
    # ------------+----------+-------------
    # BLACK MAGIC FULL FEATURED ENABLED
    def display_rows(
        menu, row_id: int, page_counter: int, menu_mode: str, height, width
    ):
        current_row_id = row_id
        current_page = page_counter
        display_menu = Menu(menu, height, width)
        display_menu.get_menu_list(stdscr, current_row_id, menu_mode)

        # Main menu mode
        if menu_mode == "main":
            while True:
                key = stdscr.getch()
                stdscr.clear()
                # TODO: Use switch, Luke!
                if key == curses.KEY_UP and current_row_id > 0:
                    current_row_id -= 1
                    stdscr.refresh()
                elif key == curses.KEY_UP and current_row_id == 0:
                    current_row_id = 2
                    stdscr.refresh()
                elif (
                    key == curses.KEY_DOWN
                    and current_row_id < len(display_menu.menu) - 1
                ):
                    current_row_id += 1
                    stdscr.refresh()
                elif key == curses.KEY_DOWN and current_row_id == 2:
                    current_row_id = 0
                    stdscr.refresh()
                # editor mode
                elif (
                    key == curses.KEY_ENTER
                    or key in [10, 13]
                    and current_row_id == len(display_menu.menu) - 3
                ):
                    alice.edit_aleases(EDITOR)
                    stdscr.refresh()
                    display_rows(MAIN_MENU, 0, 1, "main", height, width)

                # load first page of aliases
                elif (
                    key == curses.KEY_ENTER
                    or key in [10, 13]
                    and current_row_id == len(display_menu.menu) - 2
                ):
                    if ALIASES:
                        stdscr.refresh()
                        chunk = alice.alias_paginate(ALIASES, current_page)
                        if chunk:
                            display_rows(
                                chunk, 0, current_page, "aliases", height, width
                            )
                        else:
                            break
                    else:
                        stdscr.addstr(1, 0, "Sory, there are no aleases")
                        stdscr.getch()
                elif (
                    key == curses.KEY_ENTER
                    or key in [10, 13]
                    and current_row_id == len(display_menu.menu) - 1
                ):
                    stdscr.clear()
                    break
                # Some adaptive, if we want to resize window update the func with the new h, w
                elif key == curses.KEY_RESIZE:
                    stdscr.refresh()
                    height, width = stdscr.getmaxyx()
                    display_rows(
                        menu, current_row_id, current_page, menu_mode, height, width
                    )
                    break
                elif key == curses.KEY_EXIT or ord("q"):
                    break

                display_menu.get_menu_list(stdscr, current_row_id, "main")

        # Aliases menu navmode
        elif menu_mode == "aliases":
            while True:
                key = stdscr.getch()
                stdscr.clear()
                # UP condition
                if key == curses.KEY_UP and current_row_id > 0:
                    current_row_id -= 1
                    stdscr.refresh()
                elif key == curses.KEY_UP and current_row_id <= 0 and current_page == 1:
                    current_row_id = 0
                    stdscr.refresh()
                # paginate to the previuos page of aleases
                elif key == curses.KEY_UP and current_row_id <= 0:
                    stdscr.refresh()
                    current_page -= 1
                    prev_chunk = alice.alias_paginate(ALIASES, current_page)
                    if prev_chunk:
                        display_rows(
                            prev_chunk, 0, current_page, "aliases", height, width
                        )
                    else:
                        break
                # DOWN condition
                elif (
                    key == curses.KEY_DOWN
                    and current_row_id < len(display_menu.menu) - 1
                ):
                    current_row_id += 1
                    stdscr.refresh()
                # paginate to the next page of aleases
                elif key == curses.KEY_DOWN and current_row_id >= 9:
                    stdscr.refresh()
                    current_page += 1
                    next_chunk = alice.alias_paginate(ALIASES, current_page)
                    if next_chunk:
                        display_rows(
                            next_chunk, 0, current_page, "aliases", height, width
                        )
                    else:
                        break
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    stdscr.refresh()
                    for _id, row in enumerate(menu):
                        if _id == current_row_id:
                            cmdr = str(
                                re.sub(r"[^\w\s]+|[\d]+", r"", f"{str(row)}").strip()
                            )
                            stdscr.addstr(0, 0, cmdr)
                            stdscr.addstr(3, 0, "Press Enter to exec")
                            stdscr.getch()
                            curses.endwin()
                            # getting os enviroment for source aliases
                            subprocess.call([os.environ["SHELL"], "-ic", cmdr])

                # RESIZE condition
                elif key == curses.KEY_RESIZE:
                    stdscr.refresh()
                    height, width = stdscr.getmaxyx()
                    display_rows(
                        menu, current_row_id, current_page, menu_mode, height, width
                    )
                    break
                elif key == ord("q"):
                    break
                display_menu.get_menu_list(stdscr, current_row_id, "aliases")

    # Getting initial terminal window size
    height, width = stdscr.getmaxyx()

    display_rows(MAIN_MENU, 0, 1, "main", height, width)


if __name__ == "__main__":
    curses.wrapper(main)