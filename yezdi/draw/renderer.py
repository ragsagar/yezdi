import pytest

from yezdi.draw.base import AbstractDrawingKit
from yezdi.parser.ast import Title, LineStatement, LineType, Statement


class DrawingClient:
    title_coords = (300, 100)
    origin = (20, 200)
    participant_width = 40
    participant_height = 20
    flow_line_gap = 15
    participant_gap = 20

    def __init__(self, statements, drawing_kit: AbstractDrawingKit):
        self.statements = statements
        self.drawing_kit = drawing_kit
        self.participant_coords = {}
        self.drawn_participants = set()
        self.arrow_count = 0
        self.line_height = self.get_line_statement_count() * 30
        self.title_widget = None
        self.arrow_creation_funcs = {
            LineType.SOLID: self.drawing_kit.create_solid_arrow,
            LineType.DASHED: self.drawing_kit.create_dashed_arrow,
        }

    def get_line_statement_count(self):
        return len(
            [
                statement
                for statement in self.statements
                if isinstance(statement.root, LineStatement)
            ]
        )

    def interpret(self):
        for statement in self.statements:
            self.interpret_statement(statement)

    def interpret_statement(self, statement):
        # TODO interpret others
        if isinstance(statement.root, LineStatement):
            self.interpret_line(statement.root)
        elif isinstance(statement.root, Title):
            self.interpret_title(statement.root)

    def interpret_line(self, line):
        self.draw_participant(line.source)
        self.draw_participant(line.target)
        self.draw_arrow(line)

    def draw_participant(self, participant):
        if participant not in self.drawn_participants:
            coords = self.get_coords_for_participant(participant)
            actor = self.drawing_kit.create_actor(
                coords,
                self.participant_width,
                self.participant_height,
                self.line_height,
            )
            actor.set_label(participant.name)
            self.drawn_participants.add(participant)

    def get_coords_for_participant(self, participant):
        participant_coords = self.participant_coords.get(participant.name)
        if not participant_coords:
            participant_coords = self.get_next_participant_coords()
            self.participant_coords[participant.name] = participant_coords
        return participant_coords

    def get_next_participant_coords(self):
        length = len(self.participant_coords)
        y = self.origin[1]
        x = length * self.participant_width + (length + 1) * self.participant_gap
        return x, y

    def draw_arrow(self, line):
        self.arrow_count += 1
        start = self.get_arrow_coords(line.source)
        end = self.get_arrow_coords(line.target)
        arrow_creation_func = self.arrow_creation_funcs.get(line.type)
        arrow = arrow_creation_func(start, end)
        if line.info:
            arrow.set_info(line.info)

    def get_arrow_coords(self, participant):
        x, y = self.get_coords_for_participant(participant)
        x += self.participant_width / 2.0
        y -= self.flow_line_gap * self.arrow_count
        return x, y

    def interpret_title(self, title_statement):
        self.title_widget = self.drawing_kit.create_text(
            self.title_coords, title_statement
        )

    def get_rendering_object(self):
        return self.drawing_kit.get_drawing_object()

    def draw(self):
        self.drawing_kit.prepare()

    def show(self):
        self.drawing_kit.show()
