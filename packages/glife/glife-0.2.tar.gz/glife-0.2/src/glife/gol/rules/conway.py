
from ..rules_interface import Rules as RulesAbstract
from ..field import Field
from ..point import Point


class ConwayRules(RulesAbstract):

    NAME = 'CONWAY'

    def name(self) -> str:
        return self.NAME

    def calculate(self, field: Field, point: Point) -> bool:
        result = False

        environment_points = self._environment(point)
        environment_life_cells = self._get_states(field, environment_points)
        # environment_life_cells = self._sum_life_cells(environment_states)

        if field.state_point(point):
            if environment_life_cells in (2, 3):
                result = True
        else:
            if environment_life_cells == 3:
                result = True

        return result

    @staticmethod
    def _environment(point: Point) -> list:
        result = []
        for x in range(point.x - 1, point.x + 2):
            for y in range(point.y - 1, point.y + 2):
                if x != point.x or y != point.y:
                    result.append(Point(x,y))
        return result

    @staticmethod
    def _get_states(field: Field, points: list) -> int:
        sum: int = 0
        for p in points:
            if field.state_point(p):
                sum += 1
        return sum
