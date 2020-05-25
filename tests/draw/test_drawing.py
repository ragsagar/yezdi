from unittest import TestCase

from yezdi.draw.renderer import DrawingRenderer


class DrawingTestCase(TestCase):
    def test_three_participants_creates_three_rectangles(self):
        expected_rect_origins = [(10, 100), (60, 100), (110, 100)]
        statements = []
        renderer = DrawingRenderer(statements)
        ax = renderer.draw()
        assert expected_rect_origins == [
            rect.get_xy() for rect in enumerate(ax.patches)
        ]
