class Item(object):
    def __init__(self, host_info, comment=''):
        self.host_info = host_info
        self.comment = comment

    def __str__(self):
        return self.host_info + '->' + self.comment

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.host_info
        elif isinstance(other, Item):
            return self.host_info == other.host_info
        return False