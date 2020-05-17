class AST:
    pass


class Program:
    def __init__(self):
        self.statements = []
        self.participants = {}

    @staticmethod
    def get_participant():
        return


class Statement:
    pass


class Participant:
    def __init__(self, name):
        self.name = name
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)


class Line:
    def __init__(self, line_type):
        self.type = line_type
        self.target = None
        self.info = None

    def set_target(self, target):
        self.target = target

    def set_info(self, info):
        self.info = info
