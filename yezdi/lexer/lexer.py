from functools import partial

import pytest

from .token import Token, TokenType


class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.current_position, self.read_position = 0, 0
        self.current_char = None
        self.char_tokentype_map = {
            ":": partial(self._create_token, TokenType.COLON),
            ">": partial(self._create_token, TokenType.GREATER_THAN),
            "<": partial(self._create_token, TokenType.LESS_THAN),
            "-": partial(self._create_token, TokenType.HYPHEN),
            "(": partial(self._create_token, TokenType.LPAREN),
            ")": partial(self._create_token, TokenType.RPAREN),
            "": partial(self._create_token, TokenType.EOF),
        }
        self.keyword_map = {
            "title": TokenType.TITLE
        }
        self._read_character()

    def _read_character(self):
        if self.read_position > len(self.input_string) - 1:
            self.current_char = ""
        else:
            self.current_char = self.input_string[self.read_position]
        self.current_position, self.read_position = (
            self.read_position,
            self.read_position + 1,
        )

    def next_token(self):
        self.consume_space()
        token_func = self.char_tokentype_map.get(self.current_char, self._read_default)
        token = token_func(self.current_char)
        return token

    def consume_space(self):
        while self.current_char.isspace():
            self._read_character()

    def _read_default(self, current_char):
        if current_char.isalpha():
            token_type, identifier = self._read_identifier()
            # print("Token: {}, Identifier = {}".format(token_type, identifier))
            return Token(token_type, identifier)
        else:
            return Token(TokenType.ILLEGAL, "")

    def _read_identifier(self):
        start_position = self.current_position
        token_type = TokenType.IDENTIFIER
        while True:
            if self.current_char.isalpha() or self.current_char.isdigit():
                self._read_character()
            elif self._is_newline(self.current_char):
                break
            elif self.current_char.isspace():
                keyword = self.input_string[start_position: self.current_position]
                if keyword in self.keyword_map:
                    token_type = self.keyword_map.get(keyword)
                    break
                self._read_character()
            else:
                break
        return token_type, self.input_string[start_position: self.current_position]

    def _is_valid_space(self, value):
        return value.isspace() and value != "\n"

    def _is_newline(self, value):
        return value == "\n"

    def _create_token(self, token_type, literal):
        self._read_character()
        return Token(token_type, literal)
