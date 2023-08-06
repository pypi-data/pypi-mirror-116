from typing import List

from .colony_state import ColonyState
from .exception.colony_exception import ColonyException
from ..abstract.gol_interface import GameOfLife as GOLAbstract
from ..gol.field import Field


class Colony(GOLAbstract):

    def __init__(self, gol_engine: GOLAbstract):
        self.gol = gol_engine
        self._field_list: List[Field] = []
        self._field_hash_list: List[int] = []
        self._state: str = ColonyState.ALIVE
        self._add_field(self.gol.field())

    def field(self) -> Field:
        return self.gol.field()

    def next_generation(self) -> Field:
        ng: Field = self.gol.next_generation()
        self._add_field(ng)
        return ng

    def init_field(self, x: int, y: int, start_generation: Field) -> None:
        raise NotImplementedError

    def _add_field(self, field: Field) -> None:
        hash_value: int = self.generate_hash(field.__str__())
        self._field_list.append(field)
        self._field_hash_list.append(hash_value)
        self._test_if_not_dead()
        self._test_if_not_repeated()

    def _is_dead(self) -> bool:
        if '1' in self.gol.field().__str__():
            return False
        else:
            return True

    def _is_repeated(self, hash_value: int) -> bool:
        if hash_value in self._field_hash_list[:-1]:
            return True
        else:
            return False

    def _test_if_not_dead(self):
        if self._is_dead():
            self._state = ColonyState.DEAD
            raise ColonyException.is_dead()

    def _test_if_not_repeated(self):
        if self._is_repeated(self._field_hash_list[-1]):
            self._state = ColonyState.LOOPED
            raise ColonyException.is_repeated()

    @staticmethod
    def generate_hash(field: Field) -> int:
        return hash(field)
