from unittest import TestCase

from yezdi.lexer import Lexer
from yezdi.lexer.token import TokenType, Token


class LexerTestCase(TestCase):
    def test_next_token(self):
        input_string = """title API v1
        
User->Backend:
Backend->Elastic Search:
Elastic Search-->Backend:
Backend-->User:
"""
        expected_tokens = [
            Token(TokenType.TITLE, "title"),
            Token(TokenType.IDENTIFIER, "API v1"),
            Token(TokenType.IDENTIFIER, "User"),
            Token(TokenType.HYPHEN, "-"),
            Token(TokenType.GREATER_THAN, ">"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.HYPHEN, "-"),
            Token(TokenType.GREATER_THAN, ">"),
            Token(TokenType.IDENTIFIER, "Elastic Search"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.IDENTIFIER, "Elastic Search"),
            Token(TokenType.HYPHEN, "-"),
            Token(TokenType.HYPHEN, "-"),
            Token(TokenType.GREATER_THAN, ">"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.HYPHEN, "-"),
            Token(TokenType.HYPHEN, "-"),
            Token(TokenType.GREATER_THAN, ">"),
            Token(TokenType.IDENTIFIER, "User"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.EOF, ""),
        ]
        # when
        lexer = Lexer(input_string)
        # then
        for expected_token in expected_tokens:
            result = lexer.next_token()
            assert expected_token == result
