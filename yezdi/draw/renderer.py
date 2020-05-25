import pytest

from yezdi.draw.mpl_engine import MPLEngine
from yezdi.parser.ast import Participant, Title

PARTICIPANT_WIDTH = 40
PARTICIPANT_HEIGHT = 20
DOWNSTROKE_HEIGHT = 100
PARTICIPANT_GAP = 20
EDGE_COLOR = "black"
FILL_COLOR = "black"
START_COORDS = (20, 200)
FLOW_LINE_GAP = 15


class DrawingRenderer:
    def __init__(self):
        # self.statements = statements
        self.engine = MPLEngine()
        self.origin = START_COORDS
        self.participant_coords = {}
        self.drawn_participants = set()
        self.arrow_count = 0

    def interpret(self, program):
        for statement in program.statements:
            self.interpret_statement(statement)

    def interpret_statement(self, statement):
        # TODO interpret others
        if isinstance(statement.root, Participant):
            self.interpret_participant(statement.root)
        elif isinstance(statement.root, Title):
            self.interpret_title(statement.root)

    def interpret_participant(self, participant):
        if participant not in self.drawn_participants:
            coords = self.get_coords_for_participant(participant)
            print(participant.name, coords)
            self.engine.add_rectangle(
                coords, PARTICIPANT_WIDTH, PARTICIPANT_HEIGHT,
            )
            self.draw_down_stroke(coords)
            self.add_participant_label(participant.name, coords)
            self.drawn_participants.add(participant)
        current_coords = self.get_coords_for_participant(participant)
        target_coords = self.get_coords_for_participant(participant.line.target)
        print(participant.name, current_coords, target_coords)
        self.draw_arrow(current_coords, target_coords)

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

    def draw_arrow(self, source_coords, target_coords):
        self.arrow_count += 1
        sx, sy = source_coords
        sx += PARTICIPANT_WIDTH / 2.0
        sy -= FLOW_LINE_GAP * self.arrow_count
        tx, ty = target_coords
        tx += PARTICIPANT_WIDTH / 2.0
        ty -= FLOW_LINE_GAP * self.arrow_count
        self.engine.add_arrow((sx, sy), (tx, ty))

    def interpret_title(self, titleobj):
        pass

    def get_rendering_object(self):
        return self.engine.get_drawing_object()

    def draw(self):
        self.engine.prepare()

    def show(self):
        self.engine.show()
