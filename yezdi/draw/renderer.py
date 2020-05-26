import pytest

from yezdi.draw.mpl_engine import MPLEngine
from yezdi.parser.ast import Participant, Title, LineStatement

PARTICIPANT_WIDTH = 40
PARTICIPANT_HEIGHT = 20
DOWNSTROKE_HEIGHT = 100
PARTICIPANT_GAP = 20
EDGE_COLOR = "black"
FILL_COLOR = "black"
START_COORDS = (20, 200)
FLOW_LINE_GAP = 15


class DrawingRenderer:
    def __init__(self, statements):
        self.statements = statements
        self.engine = MPLEngine()
        self.origin = START_COORDS
        self.participant_coords = {}
        self.drawn_participants = set()
        self.arrow_count = 0

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
            self.engine.add_rectangle(
                coords, PARTICIPANT_WIDTH, PARTICIPANT_HEIGHT,
            )
            self.draw_down_stroke(coords)
            self.add_participant_label(participant.name, coords)
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
        x = length * PARTICIPANT_WIDTH + (length + 1) * PARTICIPANT_GAP
        return x, y

    def draw_down_stroke(self, participant_coords):
        px, py = participant_coords
        middlex = px + (PARTICIPANT_WIDTH / 2.0)
        start_coords = middlex, py
        end_coords = middlex, py - DOWNSTROKE_HEIGHT
        self.engine.add_dotted_line(start_coords, end_coords)

    def add_participant_label(self, label, participant_coords):
        x, y = participant_coords
        tx = x + (PARTICIPANT_WIDTH / 2.0)
        ty = y + (PARTICIPANT_HEIGHT / 2.0)
        self.engine.add_text(label, (tx, ty))

    def draw_arrow(self, line):
        self.arrow_count += 1
        sx, sy = self.get_coords_for_participant(line.source)
        sx += PARTICIPANT_WIDTH / 2.0
        sy -= FLOW_LINE_GAP * self.arrow_count
        tx, ty = self.get_coords_for_participant(line.target)
        tx += PARTICIPANT_WIDTH / 2.0
        ty -= FLOW_LINE_GAP * self.arrow_count
        self.engine.add_arrow((sx, sy), (tx, ty))
        lx = sx + ((tx - sx) / 2.0)
        ly = sy + ((ty - sy) / 2.0) + 1
        self.engine.add_text(line.info, (lx, ly), ha="center")

    def interpret_title(self, titleobj):
        pass

    def get_rendering_object(self):
        return self.engine.get_drawing_object()

    def draw(self):
        self.engine.prepare()

    def show(self):
        self.engine.show()
