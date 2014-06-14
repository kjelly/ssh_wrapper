#!/usr/bin/env python

import curses
import sys
from subprocess import Popen

from ui.screenWrapper import ScreenWrapper
from ui.widget import Widget
from data_struct.item import Item
from db.database import Database


class MainMenu(Widget):
    DOWN = [curses.KEY_DOWN, ord('j')]
    UP = [curses.KEY_UP, ord('k')]
    SPACE_KEY = [32]
    EXIT_KEY = [27, ord('q')]
    ENTER_KEY = [ord('\n')]
    INCR_LINE = 1
    DECR_LINE = -1

    line_list = []

    def __init__(self, screen, line_list):
        super(MainMenu, self).__init__(screen)
        print 'gg', self.screen
        self.result = None
        curses.noecho()
        curses.cbreak()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
        self.screen.keypad(1)
        self.screen.border(0)
        self.top_line_num = 0
        self.highlight_line_num = 0
        self.markedLineNums = []
        self.line_list = line_list
        self.line_list_length = len(self.line_list)

    def handle_key_event(self, c):
       if c in self.UP:
            self.updown(self.DECR_LINE)
       elif c in self.DOWN:
            self.updown(self.INCR_LINE)
       elif c in self.SPACE_KEY:
            self.mark_line()
       elif c in self.EXIT_KEY:
            self.exit()
       elif c in self.ENTER_KEY:
            self.do_selection()
            self.exit()

    def mark_line(self):
        linenum = self.top_line_num + self.highlight_line_num
        if linenum in self.markedLineNums:
            self.markedLineNums.remove(linenum)
        else:
            self.markedLineNums.append(linenum)

    def display_screen(self):
        self.screen.erase()

        # now paint the rows
        top = self.top_line_num
        bottom = self.top_line_num+curses.LINES
        for (index,item,) in enumerate(self.line_list[top:bottom]):
            line = '%s' % (str(item),)

            # highlight current line
            if index != self.highlight_line_num:
                self.screen.addstr(index, 0, line)
            else:
                self.screen.addstr(index, 0, line, curses.color_pair(1)|curses.A_BOLD)
        self.screen.refresh()

    # move highlight up/down one line
    def updown(self, increment):
        nextLineNum = self.highlight_line_num + increment

        # paging
        if increment == self.DECR_LINE and self.highlight_line_num == 0 and self.top_line_num != 0:
            self.top_line_num += self.DECR_LINE
            return
        elif increment == self.INCR_LINE and nextLineNum == curses.LINES and (self.top_line_num+curses.LINES) != self.line_list_length:
            self.top_line_num += self.INCR_LINE
            return

        # scroll highlight line
        if increment == self.DECR_LINE and (self.top_line_num != 0 or self.highlight_line_num != 0):
            self.highlight_line_num = nextLineNum
        elif increment == self.INCR_LINE and (self.top_line_num+self.highlight_line_num+1) != self.line_list_length and self.highlight_line_num != curses.LINES:
            self.highlight_line_num = nextLineNum

    def do_selection(self):
        self.result = self.line_list[self.highlight_line_num]
        self.exit()

    def get_user_choice(self):
        return self.result


class RunClass(object):
    def __init__(self, cmd):
        self.p = Popen("ssh {args}".format(args=ssh_args), shell=True)
        self.clear_flag = False

    def wait(self):
        self.p.wait()
        self.ret_code = self.p.returncode
        self.clear_flag = True
        return self.ret_code

    def __del__(self):
        if self.p.returncode is None:
            self.p.kill()
            print 'killed'


if __name__ == '__main__':
    db = Database('~/host_list.txt')

    if len(sys.argv) < 2:
        screen_wrapper = ScreenWrapper()
        with screen_wrapper as screen:
            ih = MainMenu(screen, db.get_item_list())
            ih.run()
        screen_wrapper.restore_screen()
        choice = ih.get_user_choice()
        if choice is None:
            sys.exit()
        ssh_args = choice.host_info

    else:
        ssh_args = ' '.join(sys.argv[1:])
    p = RunClass('ssh {args}'.format(args=ssh_args))
    if p.wait() == 0:
        item = Item(ssh_args, '')
        db.add_item(item)
        print db.get_item_list()
        db.write_to_file()
