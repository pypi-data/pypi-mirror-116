
import pytest
from ..point import Point
from ..field import Field


@pytest.fixture
def field():
    o = Field(Point(10,10))
    o.set(0, 3, True)
    o.set_point(Point(7, 7), True)
    return o


def test_state(field: Field):
    assert field.state(0,0) == False
    assert field.state(0,3) == True
    assert field.state(-1,0) == False


def test_iter(field: Field):
    i = s = 0
    points = []
    for p in field:
        i += 1
        if field.state_point(p):
            s += 1
            points.append(p)
    assert i == 100
    assert s == 2
    assert len(points) == 2
    assert points[0].x == 0
    assert points[0].y == 3
    assert points[1].x == 7
    assert points[1].y == 7


def test_all_on(field: Field):
    for p in field:
        field.set_point(p, True)
    assert field.state(0, 0) == True
    assert field.state(9, 9) == True
    assert field.state(0, 10) == False
    assert field.state(10, 0) == False
