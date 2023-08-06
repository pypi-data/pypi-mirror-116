
import pytest
from ...field import Field
from ...point import Point
from ...rules.conway import ConwayRules


@pytest.fixture
def field():
    o = Field(Point(3,3))
    return o


@pytest.fixture
def conway_rules():
    o = ConwayRules()
    return o


def test_01(field: Field, conway_rules: ConwayRules):
    field.init([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ])
    p = Point(1,1)
    assert field.state_point(p) == True
    if not conway_rules.calculate(field, p):
        field.set_point(p, False)
    assert field.state_point(p) == False


def test_02(field: Field, conway_rules: ConwayRules):
    field.init([
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])
    p = Point(1, 1)
    assert field.state_point(p) == True
    assert field.state(2,2) == True
    if not conway_rules.calculate(field, p):
        field.set_point(p, False)
    assert field.state_point(p) == False


def test_03(field: Field, conway_rules: ConwayRules):
    field.init([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == True


def test_04(field: Field, conway_rules: ConwayRules):
    field.init([
        [1, 0, 0],
        [0, 1, 1],
        [0, 0, 1],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == True


def test_05(field: Field, conway_rules: ConwayRules):
    field.init([
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == False


def test_06(field: Field, conway_rules: ConwayRules):
    field.init([
        [1, 0, 1],
        [1, 1, 1],
        [0, 0, 1],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == False


def test_07(field: Field, conway_rules: ConwayRules):
    field.init([
        [1, 0, 1],
        [1, 1, 0],
        [0, 1, 1],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == False


def test_08(field: Field, conway_rules: ConwayRules):
    field.init([
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == False


def test_09(field: Field, conway_rules: ConwayRules):
    field.init([
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == False


def test_10(field: Field, conway_rules: ConwayRules):
    field.init([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ])
    p = Point(1,1)
    assert field.state_point(p) == False
    assert conway_rules.calculate(field, p) == False


def test_11(field: Field, conway_rules: ConwayRules):
    field.init([
        [0, 0, 0],
        [1, 0, 1],
        [1, 0, 0],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == True


def test_12(field: Field, conway_rules: ConwayRules):
    field.init([
        [0, 0, 0],
        [1, 0, 1],
        [0, 0, 0],
    ])
    assert conway_rules.calculate(field, Point(1,1)) == False


def test_20(field: Field, conway_rules: ConwayRules):
    field.init([
        [0, 0, 0],
        [0, 1, 1],
        [0, 1, 1],
    ])
    assert conway_rules.calculate(field, Point(2,2)) == True
