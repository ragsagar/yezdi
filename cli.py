import argparse
import logging

from yezdi.draw.mpl_kit import MPLKit
from yezdi.draw.renderer import DrawingClient
from yezdi.lexer import Lexer
from yezdi.parser.parser import Parser


def get_program(input_string):
    lexer = Lexer(input_string)
    parser = Parser(lexer)
    program = parser.parse_program()
    return program


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Input file")
    args = parser.parse_args()
    return args


def read_input(input_file):
    with open(input_file) as reader:
        return reader.read()


def draw_diagram(input_string):
    program = get_program(input_string)
    drawing_kit = MPLKit(debug=False)
    renderer = DrawingClient(program.statements, drawing_kit=drawing_kit)
    renderer.interpret()
    renderer.draw()
    renderer.show()


if __name__ == "__main__":
    f = logging.Filter("yezdi")
    logging.root.addFilter(f)
    args = parse_arguments()
    input_string = read_input(args.input)
    print(input_string)
    draw_diagram(input_string)
