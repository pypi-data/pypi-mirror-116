
from abc import ABC
from abc import abstractmethod
from ..gol.field import Field
from ..gol.point import Point


class GameOfLife(ABC):

    @abstractmethod
    def field(self) -> Field:
        pass

    @abstractmethod
    def next_generation(self) -> Field:
        pass

    @abstractmethod
    def init_field(self, x: int, y: int, start_generation: Field) -> None:
        pass
