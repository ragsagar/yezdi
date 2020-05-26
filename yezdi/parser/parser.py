from yezdi.lexer.token import TokenType
from yezdi.parser.ast import Program, Statement, Participant, Title, LineStatement


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
        while self.current_token.type != TokenType.EOF:
            statement = self.parse_statement()
            if statement:
                program.statements.append(statement)
            self.next_token()
        return program

    def parse_statement(self):
        if self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_line_statement()
        elif self.current_token.type == TokenType.TITLE:
            return self.parse_title()
        return None

    def parse_line_statement(self):
        participant_literal = self.current_token.literal

        if not self.peek_token.type in [TokenType.SOLID_LINE, TokenType.DASHED_LINE]:
            return None
        self.next_token()

        participant = Participant(participant_literal)
        line = LineStatement(self.current_token.type)
        line.set_source(participant)
        if not self.expect_peek(TokenType.IDENTIFIER):
            return None
        target = Participant(self.current_token.literal)
        line.set_target(target)
        if not self.expect_peek(TokenType.COLON):
            return None
        if self.expect_peek(TokenType.IDENTIFIER):
            line.set_info(self.current_token.literal)
        if self.peek_token.type not in [TokenType.NEWLINE, TokenType.EOF]:
            return None
        statement = Statement(line)
        return statement

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
        title = Title(self.current_token.literal)
        return Statement(title)


class ParserError(Exception):
    pass
