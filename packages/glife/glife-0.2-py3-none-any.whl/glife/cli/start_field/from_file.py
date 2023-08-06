from typing import List

from ...gol.field import Field
from ...gol.point import Point


def input_field(file: str, char_false: str, char_true: str) -> Field:
    row: List = []
    field_list: List[List] = []

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        for char in line.strip():
            if char == '0':
                row.append(0)
            else:
                row.append(1)
        field_list.append(row)
        row = []

    field = Field(Point(len(field_list[0]), len(field_list)))
    field.init(field_list)
    return field
