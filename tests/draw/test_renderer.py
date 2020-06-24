from unittest import TestCase

from yezdi.draw.base import (
    AbstractDrawingKit,
    AbstractActor,
    AbstractArrow,
    AbstractText,
)
from yezdi.draw.mpl_kit import MPLText
from yezdi.draw.renderer import DrawingClient
from yezdi.lexer.token import TokenType
from yezdi.parser.ast import LineStatement, Participant, Statement, Title


class DummyDrawingKit(AbstractDrawingKit):
    def create_actor(self, coords, width, height, line_height) -> AbstractActor:
        return DummyActor(coords, width, height)

    def create_solid_arrow(self, from_point, to_point) -> AbstractArrow:
        return DummySolidArrow(from_point, to_point)

    def create_dashed_arrow(self, from_point, to_point) -> AbstractArrow:
        return DummyDashedArrow(from_point, to_point)

    def create_text(self, coords, label) -> AbstractText:
        return DummyText(coords, label)


class DummyActor(AbstractActor):
    def set_label(self, label):
        self.label = label


class DummyArrow(AbstractArrow):
    def set_info(self, text):
        self.info = text


class DummyDashedArrow(DummyArrow):
    pass


class DummySolidArrow(DummyArrow):
    pass


class DummyText(AbstractText):
    pass


class DrawingClientTestCase(TestCase):
    def setUp(self) -> None:
        self.drawing_kit = DummyDrawingKit()
        self.user_auth_statements = [
            Statement(Title("Test title"),),
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                    info="Request",
                ),
            ),
            Statement(
                LineStatement(
                    token_type=TokenType.DASHED_LINE,
                    source=Participant("Backend"),
                    target=Participant("Auth"),
                ),
            ),
            Statement(
                LineStatement(
                    token_type=TokenType.DASHED_LINE,
                    source=Participant("Auth"),
                    target=Participant("Backend"),
                ),
            ),
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("Backend"),
                    target=Participant("User"),
                    info="Response",
                ),
            ),
        ]

    def test_get_line_height_returns_minimum_for_small_statements(self):
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                ),
            ),
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("Backend"),
                    target=Participant("User"),
                ),
            ),
        ]
        expected = 80
        drawing_client = DrawingClient(
            statements=statements, drawing_kit=self.drawing_kit
        )
        self.assertEqual(drawing_client.get_line_height(), expected)

    def test_get_line_height_considers_line_statements_for_large_statements(self):
        title_statement = Statement(Title("title"))
        line_statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                ),
            )
            for i in range(10)
        ]
        statements = [title_statement] + line_statements
        expected = 200
        drawing_client = DrawingClient(
            statements=statements, drawing_kit=self.drawing_kit
        )
        self.assertEqual(drawing_client.get_line_height(), expected)

    def test_get_line_statement_count(self):
        title_statement = Statement(Title("title"))
        line_statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                ),
            )
            for i in range(10)
        ]
        statements = [title_statement] + line_statements
        expected = 10
        drawing_client = DrawingClient(
            statements=statements, drawing_kit=self.drawing_kit
        )
        self.assertEqual(drawing_client.get_line_statement_count(), expected)

    def test_drawing_single_statement_with_two_actors(self):
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                ),
            )
        ]
        drawing_client = DrawingClient(
            statements=statements, drawing_kit=self.drawing_kit
        )

        drawing_client.interpret()

        self.assertActors(drawing_client, "User", "Backend")

    def test_drawing_multiple_statement_with_two_actors(self):
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                ),
            ),
            Statement(
                LineStatement(
                    token_type=TokenType.DASHED_LINE,
                    source=Participant("Backend"),
                    target=Participant("User"),
                ),
            ),
        ]
        drawing_client = DrawingClient(
            statements=statements, drawing_kit=self.drawing_kit
        )

        drawing_client.interpret()

        self.assertActors(drawing_client, "User", "Backend")

    def test_drawing_more_than_two_actors(self):
        drawing_client = DrawingClient(
            statements=self.user_auth_statements, drawing_kit=self.drawing_kit
        )

        drawing_client.interpret()

        self.assertActors(drawing_client, "User", "Backend", "Auth")

    def assertActors(self, drawing_client, *args):
        assert len(args) == len(drawing_client.participants)
        assert args == tuple(drawing_client.participants.keys())
        for arg in args:
            participant = drawing_client.participants[arg]
            assert isinstance(participant, DummyActor)
            assert participant.label == arg

    def test_drawing_single_solid_line_with_info(self):
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                    info="TestInfo",
                ),
            )
        ]
        drawing_client = DrawingClient(
            statements=statements, drawing_kit=self.drawing_kit
        )

        drawing_client.interpret()

        assert drawing_client.arrow_count == 1
        assert isinstance(drawing_client.arrows[0], DummySolidArrow)
        assert drawing_client.arrows[0].info == "TestInfo"

    def test_drawing_single_dashed_line_with_info(self):
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                    info="Test info",
                ),
            )
        ]
        drawing_client = DrawingClient(
            statements=statements, drawing_kit=self.drawing_kit
        )

        drawing_client.interpret()

        assert drawing_client.arrow_count == 1
        assert isinstance(drawing_client.arrows[0], DummySolidArrow)
        assert drawing_client.arrows[0].info == "Test info"

    def test_drawing_arrows_multiple_arrows(self):
        drawing_client = DrawingClient(
            statements=self.user_auth_statements, drawing_kit=self.drawing_kit
        )

        drawing_client.interpret()

        assert drawing_client.arrow_count == 4
        assert len(drawing_client.arrows) == 4
        assert [
            DummySolidArrow,
            DummyDashedArrow,
            DummyDashedArrow,
            DummySolidArrow,
        ] == [arrow.__class__ for arrow in drawing_client.arrows]
        assert ["Request", None, None, "Response"] == [
            arrow.info for arrow in drawing_client.arrows
        ]

    def test_drawing_title_statement(self):
        # given
        title_statement = Statement(Title("title"))
        line_statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE,
                    source=Participant("User"),
                    target=Participant("Backend"),
                ),
            )
            for i in range(10)
        ]
        statements = [title_statement] + line_statements
        drawing_client = DrawingClient(
            statements=statements, drawing_kit=self.drawing_kit
        )
        # when
        drawing_client.interpret()
        # then
        self.assertIsInstance(drawing_client.title_widget, DummyText)
        self.assertEqual(drawing_client.title_widget.label, "title")

