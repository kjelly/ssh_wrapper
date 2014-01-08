class Widget(object):
    def __init__(self, screen):
        self.screen = screen
        self.exit_flag = False

    def exit(self):
        self.exit_flag = True

    def run(self):
        while not self.exit_flag:
            self.display_screen()
            # get user command
            c = self.screen.getch()
            self.handle_key_event(c)

    def handle_key_event(self, char):
        pass