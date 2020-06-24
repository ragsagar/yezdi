from enum import Enum

from yezdi.lexer.token import TokenType


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
    def __init__(self, root):
        self.root = root


class Title:
    def __init__(self, value):
        self.value = value


class LineType(Enum):
    DASHED = "DASHED"
    DOTTED = "DOTTED"
    SOLID = "SOLID"

    @classmethod
    def for_token_type(cls, token_type):
        return {TokenType.DASHED_LINE: cls.DASHED, TokenType.SOLID_LINE: cls.SOLID}.get(
            token_type
        )


class LineStatement:
    def __init__(self, token_type, source=None, target=None, info=None):
        self.type = LineType.for_token_type(token_type)
        self.source = source
        self.target = target
        self.info = info

    def set_source(self, source):
        self.source = source

    def set_target(self, target):
        self.target = target

    def set_info(self, info):
        self.info = info


class Participant:
    def __init__(self, name):
        self.name = name
        self.line = None
        self.lines = []

    def add_line(self, line):
        self.line = line
        self.lines.append(line)

    def __str__(self):
        return f"<Participant: {self.name}: {[str(line) for line in self.lines]}>"
