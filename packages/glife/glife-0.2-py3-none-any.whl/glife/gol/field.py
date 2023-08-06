
from .point import Point
from typing import List


class Field:

    _geometry: Point
    _field: List[List[int]]

    def __init__(self, geometry: Point):
        self._geometry = geometry
        self._create_field()

    def geometry(self) -> Point:
        return self._geometry

    def init(self, field: List[List[int]]) -> None:
        x = y = 0
        for i in field:
            for j in i:
                self.set(x, y, bool(j))
                x += 1
            y += 1
            x = 0

    def state(self, x: int, y: int) -> bool:
        result = False
        if (0 <= x < self._geometry.x) and (0 <= y < self._geometry.y):
            result = self._field[y][x] != 0
        return result

    def state_point(self, point: Point) -> bool:
        return self.state(point.x, point.y)

    def set(self, x: int, y: int, value: bool) -> None:
        if 0 <= x < self._geometry.x and 0 <= y < self._geometry.y:
            self._field[y][x] = int(value == True)

    def set_point(self, point: Point, value: bool) -> None:
        return self.set(point.x, point.y, value)

    def width(self) -> int:
        return len(self._field[0])

    def _create_field(self) -> None:
        self._field = [
            [0 for i in range(self._geometry.x)] for j in range(self._geometry.y)
        ]

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self._geometry.x * self._geometry.y:
            y = self.n // self._geometry.x
            if y > 0:
                x = self.n - (self._geometry.x * y)
            else:
                x = self.n
            result = Point(x, y)
            self.n += 1
        else:
            raise StopIteration
        return result

    def __str__(self):
        result: str = ''
        for point in self:
            if self.state_point(point):
                char = '1'
            else:
                char = '0'
            result += char
        return result
