import unittest

from yezdi.lexer import Lexer
from yezdi.lexer.token import TokenType
from yezdi.parser.parser import Parser


class ParserTestCase(unittest.TestCase):
    def test_participant_statement_with_solid_line(self):
        input_string = "User->Backend:request"
        lexer = Lexer(input_string)
        parser = Parser(lexer)
        program = parser.parse_program()
        assert len(program.statements) == 1
        statement = program.statements[0]
        assert statement.name == "User"
        assert len(statement.lines) == 1
        line = statement.lines[0]
        assert line.type == TokenType.SOLID_LINE
        assert line.target.name == "Backend"
        assert line.info == "request"

    def test_participant_statement_with_dashed_line(self):
        input_string = "User-->Backend:request"
        lexer = Lexer(input_string)
        parser = Parser(lexer)
        program = parser.parse_program()
        assert len(program.statements) == 1
        statement = program.statements[0]
        assert statement.name == "User"
        assert len(statement.lines) == 1
        line = statement.lines[0]
        assert line.type == TokenType.DASHED_LINE
        assert line.target.name == "Backend"
        assert line.info == "request"
