from unittest import TestCase

from yezdi.lexer import Lexer
from yezdi.lexer.token import TokenType, Token


class LexerTestCase(TestCase):
    def test_next_token(self):
        input_string = """title API v1
User->Backend-1:request
Backend->Elastic Search:
Elastic Search-->Backend:
Backend-->User:
"""
        expected_tokens = [
            Token(TokenType.TITLE, "title"),
            Token(TokenType.IDENTIFIER, "API v1"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "User"),
            Token(TokenType.SOLID_LINE, "->"),
            Token(TokenType.IDENTIFIER, "Backend-1"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.IDENTIFIER, "request"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.SOLID_LINE, "->"),
            Token(TokenType.IDENTIFIER, "Elastic Search"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "Elastic Search"),
            Token(TokenType.DASHED_LINE, "-->"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.DASHED_LINE, "-->"),
            Token(TokenType.IDENTIFIER, "User"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.EOF, ""),
        ]
        # when
        lexer = Lexer(input_string)
        # then
        for expected_token in expected_tokens:
            result = lexer.next_token()
            print(expected_token, result)
            assert expected_token == result

    def test_lexing_multiline(self):
        input_string = """User->Backend:request
        Backend->AuthService:authrequest"""
        expected_tokens = [
            Token(TokenType.IDENTIFIER, "User"),
            Token(TokenType.SOLID_LINE, "->"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.IDENTIFIER, "request"),
            Token(TokenType.NEWLINE, "\n"),
            Token(TokenType.IDENTIFIER, "Backend"),
            Token(TokenType.SOLID_LINE, "->"),
            Token(TokenType.IDENTIFIER, "AuthService"),
            Token(TokenType.COLON, ":"),
            Token(TokenType.IDENTIFIER, "authrequest"),
            Token(TokenType.EOF, ""),
        ]
        # when
        lexer = Lexer(input_string)
        # then
        for expected_token in expected_tokens:
            result = lexer.next_token()
            print(expected_token, result)
            assert expected_token == result
