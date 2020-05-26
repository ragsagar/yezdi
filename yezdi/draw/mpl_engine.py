import matplotlib.pyplot as plt

from yezdi.parser.ast import LineType


class MPLEngine:
    def __init__(self):
        # self.figure = plt.figure()
        # self.ax = plt.axes()
        self.figure, self.ax = plt.subplots(1)
        self.ax.set_label("Title")

    def get_drawing_object(self):
        return self.ax

    def add_rectangle(self, coords, width, height, ec="black", fc="white"):
        rectangle = plt.Rectangle(coords, width, height, ec=ec, fc=fc)
        self.ax.add_patch(rectangle)

    def add_text(self, text, coords, ha="center", color="black"):
        x, y = coords
        self.ax.text(x, y, text, ha=ha, color=color)

    def add_arrow(self, start_coords, end_coords, line_type=LineType.SOLID):
        ls = "--" if line_type == LineType.DASHED else "-"
        sx, sy = start_coords
        ex, ey = end_coords
        dx, dy = ex - sx, ey - sy
        self.ax.arrow(
            *start_coords,
            dx,
            dy,
            fc="black",
            ec="black",
            head_width=2.5,
            length_includes_head=True,
            ls=ls,
        )

    def add_dotted_line(self, start_coords, end_coords, width=1):
        x_coords, y_coords = zip(start_coords, end_coords)
        dotted_line = plt.Line2D(x_coords, y_coords, lw=width, ls="--", color="black")
        self.ax.add_line(dotted_line)

    def prepare(self):
        plt.axis("scaled")
        self.ax.set_aspect("equal", adjustable="box", anchor="C")

    def show(self):
        self.figure.waitforbuttonpress(timeout=10)
        self.figure.show()
        # plt.show()
