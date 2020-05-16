from enum import Enum


class TokenType(Enum):
    TITLE = "TITLE"
    SOLID_LINE = "SOLID_LINE"
    DASHED_LINE = "DASHED_LINE"
    COLON = "COLON"
    IDENTIFIER = "IDENTIFIER"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"


class Token:
    keyword_map = {
        "title": TokenType.TITLE,
        "->": TokenType.SOLID_LINE,
        "-->": TokenType.DASHED_LINE,
    }

    def __init__(self, token_type, literal):
        self.type = token_type
        self.literal = literal

    def __str__(self):
        return f"<Token: {self.type}({self.literal})>"

    def __eq__(self, other):
        return self.type == other.type and self.literal == other.literal
