import unittest
import pytest

from yezdi.lexer import Lexer
from yezdi.parser.ast import (
    Title,
    Statement,
    LineStatement,
    LineType,
)
from yezdi.parser.parser import Parser


def get_program(input_string):
    lexer = Lexer(input_string)
    parser = Parser(lexer)
    program = parser.parse_program()
    return program


def pytest_generate_tests(metafunc):
    # called once per each test function
    funcarglist = metafunc.cls.params[metafunc.function.__name__]
    argnames = sorted(funcarglist[0])
    metafunc.parametrize(
        argnames, [[funcargs[name] for name in argnames] for funcargs in funcarglist]
    )


class TestParserWithSingleParticipantLine:
    input_string1 = "User->Backend:request"
    input_string2 = "User-->Backend:request"
    input_string3 = "User->Backend: "

    params = {
        "test_contains_only_one_statement": [
            {"input_string": input_string1},
            {"input_string": input_string2},
        ],
        "test_statement_type": [
            {"input_string": input_string1},
            {"input_string": input_string2},
        ],
        "test_statement_root_node_is_line_statement": [
            {"input_string": input_string1},
            {"input_string": input_string2},
        ],
        "test_line_statement_source_name": [
            {"input_string": input_string1},
            {"input_string": input_string2},
        ],
        "test_line_statement_target_name": [
            {"input_string": input_string1},
            {"input_string": input_string2},
        ],
        "test_line_target_info": [
            {"input_string": input_string1, "exp_info": "request"},
            {"input_string": input_string2, "exp_info": "request"},
            {"input_string": input_string3, "exp_info": None},
        ],
        "test_line_type": [
            {"input_string": input_string1, "line_type": LineType.SOLID},
            {"input_string": input_string2, "line_type": LineType.DASHED},
        ],
    }

    def test_contains_only_one_statement(self, input_string):
        program = get_program(input_string)
        assert len(program.statements) == 1

    def test_statement_type(self, input_string):
        program = get_program(input_string)
        statement = program.statements[0]
        assert isinstance(statement, Statement)

    def test_statement_root_node_is_line_statement(self, input_string):
        program = get_program(input_string)
        statement = program.statements[0]
        assert isinstance(statement.root, LineStatement)

    def test_line_statement_source_name(self, input_string):
        program = get_program(input_string)
        statement = program.statements[0]
        assert statement.root.source.name == "User"

    def test_line_statement_target_name(self, input_string):
        program = get_program(input_string)
        statement = program.statements[0]
        assert statement.root.target.name == "Backend"

    def test_line_target_info(self, input_string, exp_info):
        program = get_program(input_string)
        statement = program.statements[0]
        assert statement.root.info == exp_info

    def test_line_type(self, input_string, line_type):
        program = get_program(input_string)
        statement = program.statements[0]
        assert statement.root.type == line_type


class TestParserWithMultiLine1(unittest.TestCase):
    input_string = """User->Backend:request
    Backend->User:response"""

    @classmethod
    def setUpClass(cls):
        cls.program = get_program(cls.input_string)

    def test_contains_multiple_statements(self):
        assert len(self.program.statements) == 2

    def test_statement_types(self):
        statements = self.program.statements
        assert isinstance(statements[0].root, LineStatement)
        assert isinstance(statements[1].root, LineStatement)

    def test_line_types(self):
        statements = self.program.statements
        assert statements[0].root.type == LineType.SOLID
        assert statements[1].root.type == LineType.SOLID


class TestParserWithMultiLine2(unittest.TestCase):
    input_string = """User-->Backend:request
    Backend->Auth:response
    Auth->Backend:
    """

    @classmethod
    def setUpClass(cls):
        cls.program = get_program(cls.input_string)

    def test_contains_multiple_statements(self):
        assert len(self.program.statements) == 3

    def test_statement_types(self):
        statements = self.program.statements
        assert isinstance(statements[0].root, LineStatement)
        assert isinstance(statements[1].root, LineStatement)
        assert isinstance(statements[2].root, LineStatement)

    def test_line_types(self):
        statements = self.program.statements
        assert statements[0].root.type == LineType.DASHED
        assert statements[1].root.type == LineType.SOLID
        assert statements[2].root.type == LineType.SOLID

    def test_first_statement_source_and_target(self):
        line_statement = self.program.statements[0].root
        assert line_statement.source.name == "User"
        assert line_statement.target.name == "Backend"

    def test_second_statement_source_and_target(self):
        line_statement = self.program.statements[1].root
        assert line_statement.source.name == "Backend"
        assert line_statement.target.name == "Auth"

    def test_third_statement_source_and_target(self):
        line_statement = self.program.statements[2].root
        assert line_statement.source.name == "Auth"
        assert line_statement.target.name == "Backend"

    def test_line_infos(self):
        statements = self.program.statements
        assert statements[0].root.info == "request"
        assert statements[1].root.info == "response"
        assert statements[2].root.info == None


class TestParserWithMultiLine3(unittest.TestCase):
    input_string = """title API v1
    User->Backend:
    Backend->User:"""

    @classmethod
    def setUpClass(cls):
        cls.program = get_program(cls.input_string)

    def test_contains_multiple_statements(self):
        assert len(self.program.statements) == 3

    def test_statement_types(self):
        statements = self.program.statements
        assert isinstance(statements[0].root, Title)
        assert isinstance(statements[1].root, LineStatement)
        assert isinstance(statements[2].root, LineStatement)

    def test_title_text(self):
        statements = self.program.statements
        assert statements[0].root.value == "API v1"

    def test_line_infos(self):
        statements = self.program.statements
        assert statements[1].root.info == None
        assert statements[2].root.info == None
