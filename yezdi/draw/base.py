from abc import ABC
from typing import Any


class AbstractActor:
    """
    Rectangle with label and downstroke.
    """

    def __init__(self, origin, width, height):
        self.origin = origin
        self.width = width
        self.height = height

    def set_label(self, label):
        raise NotImplementedError


class AbstractArrow:
    def __init__(self, from_point, to_point):
        self.from_point = from_point
        self.to_point = to_point

    def set_info(self, text):
        raise NotImplementedError


class AbstractLine:
    pass


class AbstractText:
    def __init__(self, coords, label):
        self.coords = coords
        self.label = label
        self._draw_text_widget()

    def _draw_text_widget(self):
        raise NotImplementedError


class AbstractRectangle:
    def __init__(self, origin, width, height):
        self.origin = origin
        self.width = width
        self.height = height

    def add_label(self, label):
        raise NotImplementedError


class AbstractDrawingKit(ABC):
    def create_rectangle(self, origin, width, height) -> AbstractRectangle:
        raise NotImplementedError

    def create_actor(self, origin, width, height, line_height) -> AbstractActor:
        raise NotImplementedError

    def create_horizontal_line(self, from_point, to_point) -> AbstractLine:
        raise NotImplementedError

    def create_dashed_arrow(self, from_point, to_point) -> AbstractArrow:
        raise NotImplementedError

    def create_solid_arrow(self, from_point, to_point) -> AbstractArrow:
        raise NotImplementedError

    def create_text(self, coords, label) -> AbstractText:
        raise NotImplementedError

    def get_drawing_object(self) -> Any:
        raise NotImplementedError

    def prepare(self):
        raise NotImplementedError

    def show(self):
        raise NotImplementedError
