import pytest

from yezdi.lexer.token import TokenType
from yezdi.parser.ast import Program, Statement, Participant, Line, TitleStatement


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()
        self.participants = {}

    def next_token(self):
        self.current_token, self.peek_token = self.peek_token, self.lexer.next_token()

    def parse_program(self):
        program = Program()
        # pytest.set_trace()
        while self.current_token.type != TokenType.EOF:
            statement = self.parse_statement()
            if statement:
                program.statements.append(statement)
            self.next_token()
        return program

    def parse_statement(self):
        if self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_participant()
        elif self.current_token.type == TokenType.TITLE:
            return self.parse_title()

    def parse_participant(self):
        participant_literal = self.current_token.literal

        if not self.peek_token.type in [TokenType.SOLID_LINE, TokenType.DASHED_LINE]:
            return None
        self.next_token()

        participant = self.get_participant(participant_literal)
        line = Line(self.current_token.type)
        if not self.expect_peek(TokenType.IDENTIFIER):
            return None
        target = self.get_participant(self.current_token.literal)
        line.set_target(target)
        if not self.expect_peek(TokenType.COLON):
            return None
        if self.expect_peek(TokenType.IDENTIFIER):
            line.set_info(self.current_token.literal)
        if self.peek_token.type not in [TokenType.NEWLINE, TokenType.EOF]:
            return None
        participant.add_line(line)
        return participant

    def get_participant(self, value):
        if value in self.participants:
            return self.participants[value]
        else:
            participant = Participant(value)
            self.participants[value] = participant
        return participant

    def expect_peek(self, token_type):
        if self.peek_token.type == token_type:
            self.next_token()
            return True
        else:
            return False

    def parse_title(self):
        if not self.expect_peek(TokenType.IDENTIFIER):
            return None
        title = TitleStatement(self.current_token.literal)
        return title

class ParserError(Exception):
    pass
