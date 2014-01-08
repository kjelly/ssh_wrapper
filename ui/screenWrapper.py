import curses


class ScreenWrapper(object):
    def __init__(self):
        self.screen = curses.initscr()
        curses.start_color()
        self.clear_flag = False

    def restore_screen(self):
        self.clear_flag = True
        curses.initscr()
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def get_screen(self):
        return self.screen

    def __enter__(self):
        return self.screen

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.restore_screen()
