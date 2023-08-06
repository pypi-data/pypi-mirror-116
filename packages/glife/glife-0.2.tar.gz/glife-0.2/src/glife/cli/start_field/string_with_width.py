from typing import List

from ...gol.field import Field
from ...gol.point import Point


def input_field(string: str, width: int) -> Field:
    row: List = []
    field_list: List[List] = []

    for char in string:
        if char == '0' or char == '1':
            row.append(int(char))
        if len(row) == width:
            field_list.append(row)
            row = []

    if len(row) > 0:
        field_list.append(row)

    field = Field(Point(len(field_list[0]), len(field_list)))
    field.init(field_list)
    return field
