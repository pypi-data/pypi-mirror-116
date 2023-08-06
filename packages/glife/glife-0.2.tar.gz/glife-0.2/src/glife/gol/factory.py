from .arguments import Arguments
from .field import Field
from ..abstract.gol_interface import GameOfLife as GOLInterface
from .api import GameOfLife
from .rules.conway import ConwayRules
from ..cli.start_field.string_with_width import input_field


class Factory:

    @staticmethod
    def create(width: int, height: int) -> GOLInterface:
        rules = ConwayRules()
        return GameOfLife(width, height, rules)

    @staticmethod
    def create_with_start_generation(start_generation: Field) -> GOLInterface:
        rules = ConwayRules()
        gol = GameOfLife(0, 0, rules)
        gol.init_field(0, 0, start_generation)
        return gol

    @classmethod
    def create_from_arguments(cls, arguments: Arguments) -> GOLInterface:
        start_generation = input_field(arguments.start_generation, arguments.width)
        return cls.create_with_start_generation(start_generation)
