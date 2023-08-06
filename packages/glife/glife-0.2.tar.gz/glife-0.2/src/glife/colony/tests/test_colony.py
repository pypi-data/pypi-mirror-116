import pytest

from ..colony import Colony
from ..exception.colony_exception import ColonyException
from ...gol.factory import Factory
from ...gol.field import Field
from ...gol.point import Point


def test_empty():
    with pytest.raises(ColonyException) as colony_exception:
        gol = Factory.create(1, 1)
        Colony(gol)
    assert colony_exception.value.code == ColonyException.DEAD


def test_not_empty():
    field = Field(Point(1, 1))
    field.set(0, 0, True)
    gol = Factory.create_with_start_generation(field)
    colony = Colony(gol)
    assert type(colony) == Colony


def test_init_not_implemented():
    with pytest.raises(NotImplementedError):
        field = Field(Point(1, 1))
        field.set(0, 0, True)
        gol = Factory.create_with_start_generation(field)
        colony = Colony(gol)
        colony.init_field(0, 0, field)


def test_field():
    field = Field(Point(1, 1))
    field.set(0, 0, True)
    gol = Factory.create_with_start_generation(field)
    colony = Colony(gol)
    assert field == colony.field()


def test_next_generation():
    with pytest.raises(ColonyException) as colony_exception:
        field = Field(Point(1, 1))
        field.set(0, 0, True)
        gol = Factory.create_with_start_generation(field)
        colony = Colony(gol)
        colony.next_generation()
    assert colony_exception.value.code == ColonyException.DEAD


def test_next_generation_repeated():
    with pytest.raises(ColonyException) as colony_exception:
        field = Field(Point(3, 3))
        field.set(0, 1, True)
        field.set(1, 1, True)
        field.set(2, 1, True)
        gol = Factory.create_with_start_generation(field)
        colony = Colony(gol)
        colony.next_generation()
        colony.next_generation()
    assert colony_exception.value.code == ColonyException.LOOP
