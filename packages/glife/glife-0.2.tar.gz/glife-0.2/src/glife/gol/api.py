
from typing import List
from .point import Point
from .field import Field
from .rules_interface import Rules
from ..abstract.gol_interface import GameOfLife as GOLAbstract


class GameOfLife(GOLAbstract):

    _field: Field
    _rules: Rules

    def __init__(self, width: int, height: int, rules: Rules):
        self._field = Field(Point(width, height))
        self._rules = rules

    def field(self) -> Field:
        return self._field

    def next_generation(self) -> Field:
        ng = Field(self._field.geometry())
        for p in self._field:
            ng.set_point(p, self._rules.calculate(self._field, p))
        self._field = ng
        return self._field

    def init_field(self, x: int, y: int, start_generation: Field) -> None:
        self._field = start_generation
