from enum import Enum


class TokenType(Enum):
    TITLE = "TITLE"
    SOLID_LINE = "SOLID_LINE"
    DASHED_LINE = "DASHED_LINE"
    COLON = "COLON"
    IDENTIFIER = "IDENTIFIER"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    HYPHEN = "HYPHEN"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"


class Token:
    def __init__(self, token_type, literal):
        self.type = token_type
        self.literal = literal

    def __str__(self):
        return f"<Token: {self.type}({self.literal})>"

    def __eq__(self, other):
        return self.type == other.type and self.literal == other.literal
