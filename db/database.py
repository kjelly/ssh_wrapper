from data_struct.item import Item


class Database(object):
    def __init__(self, file_name):
        self.file_name = file_name
        with open(file_name, 'r') as ftr:
            outputLines = [x.strip() for x in ftr.readlines()]
        data = filter(filter_host_data, outputLines)
        self.item_list = map(parse_data, data)

    def get_item_list(self):
        return self.item_list

    def write_to_file(self):
        with open(self.file_name, 'w') as ftr:
            for i in self.item_list:
                ftr.write(str(i) + '\n')

    def add_item(self, item):
        if not item in self.item_list:
            self.item_list.append(item)


def filter_host_data(line):
    if len(line) == 0:
        return False
    if line[0] == '#':
        return False
    return True


def parse_data(data):
    parts = data.split('->')
    if len(parts) == 1:
        return Item(parts[0].strip())
    return Item(parts[0].strip(), parts[-1])