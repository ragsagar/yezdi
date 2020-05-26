from unittest import TestCase

import numpy as np

from yezdi.draw.renderer import DrawingRenderer
from yezdi.lexer.token import TokenType
from yezdi.parser.ast import LineStatement, Participant, Statement


class RendereringTestCase(TestCase):
    def test_line_statement_creates_two_rectangles(self):
        expected_rect_origins = [(20, 200), (80, 200)]
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE, source=Participant("User"), target=Participant("Backend")
                )
            )
        ]
        renderer = DrawingRenderer(statements)
        renderer.interpret()
        renderer.draw()
        ax = renderer.get_rendering_object()
        assert expected_rect_origins == [rect.get_xy() for rect in ax.patches]

    def test_line_statement_creates_correct_downstrokes(self):
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE, source=Participant("User"), target=Participant("Backend")
                )
            )
        ]
        expected_line_coords = [((40.0, 200.0), (40.0, 100.0)), ((100.0, 200.0), (100.0, 100.0))]
        renderer = DrawingRenderer(statements)
        renderer.interpret()
        renderer.draw()
        ax = renderer.get_rendering_object()
        result = []
        for line in ax.lines:
            x_plot, y_plot = line.get_xydata().T
            x1, x2 = x_plot
            y1, y2 = y_plot
            result.append(((x1, y1), (x2, y2)))
        assert expected_line_coords == result

    def test_list_statement_adds_participant_labels(self):
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE, source=Participant("User"), target=Participant("Backend")
                )
            )
        ]
        expected = [
            ("User", (40.0, 210.0)),
            ("Backend", (100.0, 210.0)),
        ]
        renderer = DrawingRenderer(statements)
        renderer.interpret()
        renderer.draw()
        ax = renderer.get_rendering_object()
        result = [(text_obj._text, (text_obj._x, text_obj._y)) for text_obj in ax.texts]
        assert result == expected

    def test_list_statement_add_required_arrows(self):
        statements = [
            Statement(
                LineStatement(
                    token_type=TokenType.SOLID_LINE, source=Participant("User"), target=Participant("Backend")
                )
            )
        ]
        renderer = DrawingRenderer(statements)
        renderer.interpret()
        renderer.draw()
        ax = renderer.get_rendering_object()
        result = ax.artists[0].get_xy().T
        # TODO: Find a way to check origin.
        assert result[0][4], result[1][0] == (40.0, 185.0)
