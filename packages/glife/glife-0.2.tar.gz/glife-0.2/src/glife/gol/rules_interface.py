
from abc import ABC
from abc import abstractmethod
from .field import Field
from .point import Point


class Rules(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def calculate(self, field: Field, point: Point) -> bool:
        pass
