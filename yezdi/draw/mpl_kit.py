import logging
from typing import Any

from yezdi.draw.base import (
    AbstractDrawingKit,
    AbstractRectangle,
    AbstractArrow,
    AbstractActor,
    AbstractText,
)
import matplotlib.pyplot as plt

from yezdi.draw.utils import calculate_dx_dy

logger = logging.getLogger(__name__)


class MPLKit(AbstractDrawingKit):
    def __init__(self, title="Diagram", debug=False):
        self.figure, self.ax = plt.subplots(1)
        self.ax.set_label(title)
        self.debug = debug

    def create_rectangle(self, origin, width, height):
        return MPLRectangle(self.ax, origin, width, height)

    def create_actor(self, coords, width, height, line_height):
        return MPLActor(self.ax, coords, width, height, line_height)

    def create_solid_arrow(self, from_point, to_point):
        return MPLSolidArrow(self.ax, from_point, to_point)

    def create_dashed_arrow(self, from_point, to_point):
        return MPLDashedArrow(self.ax, from_point, to_point)

    def get_drawing_object(self) -> Any:
        return self.figure

    def prepare(self):
        plt.axis("scaled")
        self.ax.set_aspect("equal", adjustable="box", anchor="C")
        if not self.debug:
            self.ax.get_xaxis().set_visible(False)
            self.ax.get_yaxis().set_visible(False)
            # self.figure.patch.set_visible(False)
            self.ax.axis("off")

    def show(self):
        # self.figure.waitforbuttonpress(timeout=10)
        # self.figure.show()
        plt.show()


class MPLRectangle(AbstractRectangle):
    def __init__(self, axes, origin, width, height):
        self.ax = axes
        super().__init__(origin, width, height)


class MPLActor(AbstractActor):
    def __init__(self, axes, coords, width, height, line_height):
        self.ax = axes
        self.coords = coords
        self.height = height
        self.width = width
        self.label = None
        self.line_height = line_height
        self.draw_rectangle()

    def set_label(self, label):
        self.label = label
        x, y = self.get_label_coords()
        self.text_widget = self.ax.text(x, y, label, ha="center", color="black")

    def draw_rectangle(self):
        self.rectangle = plt.Rectangle(
            self.coords, self.width, self.height, ec="black", fc="white"
        )
        self.ax.add_patch(self.rectangle)
        self.draw_actor_line()

    def get_label_coords(self):
        x, y = self.coords
        tx = x + (self.width / 2.0)
        ty = y + (self.height / 2.0)
        return tx, ty

    def draw_actor_line(self):
        start_coords, end_coords = self.get_vertical_line_coords()
        logger.debug("Drawing actor line from %s to %s", start_coords, end_coords)
        self.draw_line(start_coords, end_coords)

    def get_vertical_line_coords(self):
        x, y = self.coords
        middle_x = x + (self.width / 2.0)
        start_coords = middle_x, y
        end_coords = middle_x, y - self.line_height
        return start_coords, end_coords

    def draw_line(self, start_coords, end_coords):
        x_coords, y_coords = zip(start_coords, end_coords)
        dotted_line = plt.Line2D(x_coords, y_coords, lw=1, ls="--", color="black")
        self.ax.add_line(dotted_line)


class MPLSolidArrow(AbstractArrow):
    line_style = "-"

    def __init__(self, axes, from_point, to_point):
        self.ax = axes
        self.from_point = from_point
        self.to_point = to_point
        dx, dy = calculate_dx_dy(from_point, to_point)
        logger.debug("Drawing arrow from %s to %s", from_point, to_point)
        self.ax.arrow(
            *from_point,
            dx,
            dy,
            fc="black",
            ec="black",
            head_width=2.5,
            length_includes_head=True,
            ls=self.line_style,
        )

    def set_info(self, text):
        x, y = self.get_coords_for_info()
        self.ax.text(x, y, text, ha="center", color="black")

    def get_coords_for_info(self):
        start_x, start_y = self.from_point
        end_x, end_y = self.to_point
        gap_above_line = 1
        x = start_x + ((end_x - start_x) / 2.0)
        y = start_y + ((end_y - start_y) / 2.0) + gap_above_line
        return x, y


class MPLDashedArrow(MPLSolidArrow):
    line_style = "--"


class MPLText(AbstractText):
    def __init__(self, ax, *args, color="black", ha="center", **kwargs):
        self.ax = ax
        self.color = color
        self.ha = ha
        super().__init__(*args, **kwargs)

    def _draw_text_widget(self):
        logger.debug("Adding text %s at %s", self.label, self.coords)
        x, y = self.coords
        self.ax.text(x, y, self.label, ha=self.ha, color=self.color)
